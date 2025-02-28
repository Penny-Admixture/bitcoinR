#!/usr/bin/env python3
# Copyright (c) 2018 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the blocksdir option.
"""

import os
import shutil

from test_framework.test_framework import bitcoinRTestFramework, initialize_datadir


class BlocksdirTest(bitcoinRTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 1

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def run_test(self):
        self.stop_node(0)
        shutil.rmtree(self.nodes[0].datadir)
        initialize_datadir(self.options.tmpdir, 0)
        self.log.info("Starting with non exiting blocksdir ...")
        blocksdir_path = os.path.join(self.options.tmpdir, 'blocksdir')
        self.nodes[0].assert_start_raises_init_error(["-blocksdir=" + blocksdir_path], 'Error: Specified blocks directory "{}" does not exist.'.format(blocksdir_path))
        os.mkdir(blocksdir_path)
        self.log.info("Starting with exiting blocksdir ...")
        self.start_node(0, ["-blocksdir=" + blocksdir_path])
        self.log.info("mining blocks..")
        self.nodes[0].generate(10)
        assert os.path.isfile(os.path.join(blocksdir_path, "regtest", "blocks", "blk00000.dat"))
        assert os.path.isdir(os.path.join(self.nodes[0].datadir, "regtest", "blocks", "index"))


if __name__ == '__main__':
    BlocksdirTest().main()
