# SAMD Sercom configuration
#
# Copyright (C) 2019  Florian Heilmann <Florian.Heilmann@gmx.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

class SamdSERCOM:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split()[1]

        self.tx_pin = config.get("tx_pin")
        self.rx_pin = config.get("rx_pin", None)
        self.clk_pin = config.get("clk_pin")

        ppins = self.printer.lookup_object("pins")
        tx_pin_params = ppins.lookup_pin(self.tx_pin)
        self.mcu = tx_pin_params['chip']
        self.mcu.add_config_cmd(
            "set_sercom_pin bus=%s sercom_pin_type=tx pin=%s" % (
                self.name, self.tx_pin))

        clk_pin_params = ppins.lookup_pin(self.clk_pin)
        if self.mcu is not clk_pin_params['chip']:
           raise ppins.error("%s: SERCOM pins must be on same mcu" % (
                    config.get_name(),))
        self.mcu.add_config_cmd(
            "set_sercom_pin bus=%s sercom_pin_type=clk pin=%s" % (
                self.name, self.clk_pin))

        if self.rx_pin:
            rx_pin_params = ppins.lookup_pin(self.rx_pin)
            if self.mcu is not rx_pin_params['chip']:
                raise ppins.error("%s: SERCOM pins must be on same mcu" % (
                    config.get_name(),))
            self.mcu.add_config_cmd(
                "set_sercom_pin bus=%s sercom_pin_type=rx pin=%s" % (
                    self.name, self.rx_pin))

def load_config_prefix(config):
    return SamdSERCOM(config)