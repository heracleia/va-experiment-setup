import signal
from subprocess import Popen, PIPE
import subprocess
from muselsl import stream, list_muses
import time
from muselsl import record
import os
import csv
import bleak, asyncio
import numpy as np  # Module that simplifies computations on matrices
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import asyncio
from signal import signal, SIGPIPE, SIG_DFL


addr = '00:55:DA:BB:1E:CC'

class MuseDataCollection():
    def connect(self):
        print('Starting BlueMuse.')
        # subprocess.call('start bluemuse:', shell=True)
        subprocess.call('start bluemuse://start?streamfirst=true', shell=True)
        time.sleep(30)
        # subprocess.call('muselsl stream')

    def record(self):
        muses = stream.list_muses()
        stream.stream(muses[0]['address'])

        # Note: Streaming is synchronous, so code here will not execute until after the stream has been closed
        print('Stream has ended')
        subprocess.call('muselsl record --duration 60', shell=True)

    def stopConnection(self):
        subprocess.call('start bluemuse://shutdown', shell=True)

    def collectNeuroData(self):
        """ 1. CONNECT TO EEG STREAM """
        Delta = 0
        Theta = 1
        Alpha = 2
        Beta = 3
        """ EXPERIMENTAL PARAMETERS """
        # Modify these to change aspects of the signal processing

        # Length of the EEG data buffer (in seconds)
        # This buffer will hold last n seconds of data and be used for calculations
        BUFFER_LENGTH = 5

        # Length of the epochs used to compute the FFT (in seconds)
        EPOCH_LENGTH = 1

        # Amount of overlap between two consecutive epochs (in seconds)
        OVERLAP_LENGTH = 0.8

        # Amount to 'shift' the start of each next consecutive epoch
        SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

        # Index of the channel(s) (electrodes) to be used
        # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
        INDEX_CHANNEL = [0]
        p = os.popen('muselsl stream')
        # Search for active LSL streams
        print('Looking for an EEG stream...')
        streams = resolve_byprop('type', 'EEG', timeout=2)
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')

        # Set active EEG stream to inlet and apply time correction
        print("Start acquiring data")
        inlet = StreamInlet(streams[0], max_chunklen=12)
        eeg_time_correction = inlet.time_correction()

        # Get the stream info and description
        info = inlet.info()
        description = info.desc()

        # Get the sampling frequency
        # This is an important value that represents how many EEG data points are
        # collected in a second. This influences our frequency band calculation.
        # for the Muse 2016, this should always be 256
        fs = int(info.nominal_srate())

        """ 2. INITIALIZE BUFFERS """

        # Initialize raw EEG data buffer
        eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
        filter_state = None  # for use with the notch filter

        # Compute the number of epochs in "buffer_length"
        n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                                  SHIFT_LENGTH + 1))

        # Initialize the band power buffer (for plotting)
        # bands will be ordered: [delta, theta, alpha, beta]
        band_buffer = np.zeros((n_win_test, 4))

        """ 3. GET DATA """

        # The try/except structure allows to quit the while loop by aborting the
        # script with <Ctrl-C>
        #print('Press Ctrl-C in the console to break the while loop.')
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        FILE_NAME = ("neuroFeedback_data-" + timestamp + ".csv")
        f = open(FILE_NAME, 'w')

        # create the csv writer
        writer = csv.writer(f)
        header = ['Delta', 'Alpha', 'Beta', 'Theta']
        writer.writerow(header)

        try:
            signal(SIGPIPE, SIG_DFL)
            # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
            duration = 60
            t_end = time.time() + duration
            while time.time() < t_end:
                """ 3.1 ACQUIRE DATA """
                # Obtain EEG data from the LSL stream
                eeg_data, timestamp = inlet.pull_chunk(
                    timeout=1, max_samples=int(SHIFT_LENGTH * fs))

                # Only keep the channel we're interested in
                ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

                # Update EEG buffer with the new data
                eeg_buffer, filter_state = utils.update_buffer(
                    eeg_buffer, ch_data, notch=True,
                    filter_state=filter_state)

                """ 3.2 COMPUTE BAND POWERS """
                # Get newest samples from the buffer
                data_epoch = utils.get_last_data(eeg_buffer,
                                                 EPOCH_LENGTH * fs)

                # Compute band powers
                band_powers = utils.compute_band_powers(data_epoch, fs)
                band_buffer, _ = utils.update_buffer(band_buffer,
                                                     np.asarray([band_powers]))
                # Compute the average band powers for all epochs in buffer
                # This helps to smooth out noise
                smooth_band_powers = np.mean(band_buffer, axis=0)

                # print('Delta: ', band_powers[Band.Delta], ' Theta: ', band_powers[Band.Theta],
                #       ' Alpha: ', band_powers[Band.Alpha], ' Beta: ', band_powers[Band.Beta])

                """ 3.3 COMPUTE NEUROFEEDBACK METRICS """
                # These metrics could also be used to drive brain-computer interfaces

                # Alpha Protocol:
                # Simple redout of alpha power, divided by delta waves in order to rule out noise
                print('Delta: ', smooth_band_powers[Delta])
                print('Alpha: ', smooth_band_powers[Alpha])
                print('Beta: ', smooth_band_powers[Beta])
                print('Theta: ', smooth_band_powers[Theta])
                row=[]
                row.append(smooth_band_powers[Delta])
                row.append(smooth_band_powers[Alpha])
                row.append(smooth_band_powers[Beta])
                row.append(smooth_band_powers[Theta])
                # write a row to the csv file
                writer.writerow(row)
                row.clear()
        except (BrokenPipeError, IOError, KeyboardInterrupt) as e:
            pass

    def recordData(self):
        # without this, already connected device won't connect
        if 1: subprocess.call(['bluetoothctl', 'disconnect', addr])

        async def awrap():
            async with bleak.BleakClient(addr) as cl:
                print('Connection established')

        asyncio.run(awrap())
        muses = list_muses()
        print("Available Muses:", muses)
        p = os.popen('muselsl stream')
        time.sleep(15)
        duration = 60

test = MuseDataCollection()
test.recordData()
test.collectNeuroData()

#test.recordData()
