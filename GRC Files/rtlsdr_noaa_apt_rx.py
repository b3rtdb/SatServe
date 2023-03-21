#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RTLSDR NOAA APT Receiver V1.0.0
# Author: Dom Robinson
# Description: APT to WAV recorder for Raspberry-Noaa -V2
# GNU Radio version: 3.10.5.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy




class rtlsdr_noaa_apt_rx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "RTLSDR NOAA APT Receiver V1.0.0", catch_exceptions=True)

        ###############################################################
	    # Variables - added for Raspberry-Noaa-V2 manually after export
	    ###############################################################
        stream_name = sys.argv[1]
        gain = float(sys.argv[2])
        import decimal
        freq = int(decimal.Decimal(sys.argv[3].strip("M"))*decimal.Decimal(1000000))
        freq_offset = int(sys.argv[4])
        sdr_dev_id = sys.argv[5]
        bias_t_string = sys.argv[6]
        
        ##################################################
        # Variables
        ##################################################
        self.trans = trans = 25000
        self.samp_rate = samp_rate = 912000
        self.recfile = recfile = stream_name
        self.gain = gain
        self.freq_offset = freq_offset = 0
        self.cutoff = cutoff = 95000
        self.centre_freq = centre_freq = freq

        ##################################################
        # Blocks
        ##################################################

        self.soapy_airspyhf_source_0 = None
        dev = 'driver=airspyhf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_airspyhf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_airspyhf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_airspyhf_source_0.set_gain_mode(0, True)
        self.soapy_airspyhf_source_0.set_frequency(0, centre_freq)
        self.soapy_airspyhf_source_0.set_frequency_correction(0, freq_offset)
        self.soapy_airspyhf_source_0.set_gain(0, 'RF', min(max(0, -48.0), 0.0))
        self.soapy_airspyhf_source_0.set_gain(0, 'LNA', 6 if True else 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=4,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=441,
                decimation=192,
                taps=[],
                fractional_bw=0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            20,
            firdes.low_pass(
                1,
                samp_rate,
                cutoff,
                trans,
                window.WIN_HAMMING,
                6.76))
        self.gr_wavfile_sink_0_0_0_0 = blocks.wavfile_sink(
            recfile,
            1,
            11025,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.7)
        self.blks2_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=96000,
        	audio_decimation=5,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.gr_wavfile_sink_0_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blks2_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.soapy_airspyhf_source_0, 0), (self.low_pass_filter_0, 0))


    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.trans, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.trans, window.WIN_HAMMING, 6.76))
        self.soapy_airspyhf_source_0.set_sample_rate(0, self.samp_rate)

    def get_recfile(self):
        return self.recfile

    def set_recfile(self, recfile):
        self.recfile = recfile
        self.gr_wavfile_sink_0_0_0_0.open(self.recfile)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_airspyhf_source_0.set_gain(0, 'RF', min(max(self.gain, -48.0), 0.0))

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.soapy_airspyhf_source_0.set_frequency_correction(0, self.freq_offset)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.trans, window.WIN_HAMMING, 6.76))

    def get_centre_freq(self):
        return self.centre_freq

    def set_centre_freq(self, centre_freq):
        self.centre_freq = centre_freq
        self.soapy_airspyhf_source_0.set_frequency(0, self.centre_freq)




def main(top_block_cls=rtlsdr_noaa_apt_rx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()