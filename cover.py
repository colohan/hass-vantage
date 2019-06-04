"""
Support for Vantage shades.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/cover.vantage/
"""
import logging

from homeassistant.components.cover import (
    CoverDevice, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_STOP, SUPPORT_SET_POSITION,
    ATTR_POSITION)
from ..vantage import (
    VantageDevice, VANTAGE_DEVICES, VANTAGE_CONTROLLER)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['vantage']


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Vantage shades."""
    devs = []
    for (area_name, device) in hass.data[VANTAGE_DEVICES]['cover']:
        dev = VantageCover(area_name, device, hass.data[VANTAGE_CONTROLLER])
        devs.append(dev)

    add_devices(devs, True)
    return True


class VantageCover(VantageDevice, CoverDevice):
    """Representation of a Vantage shade."""

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP | SUPPORT_SET_POSITION

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        if self._vantage_device.last_level() is None:
            return None
        return self._vantage_device.last_level() < 1

    @property
    def current_cover_position(self):
        """Return the current position of cover."""
        return self._vantage_device.last_level()

    def close_cover(self, **kwargs):
        """Close the cover."""
        self._vantage_device.level = 0

    def stop_cover(self, **kwargs):
        """stop the cover."""
        self._vantage_device.level = None
        self._vantage_device.stop()

    def open_cover(self, **kwargs):
        """Open the cover."""
        self._vantage_device.level = 100

    def set_cover_position(self, **kwargs):
        """Move the shade to a specific position."""
        if ATTR_POSITION in kwargs:
            position = kwargs[ATTR_POSITION]
            self._vantage_device.level = position

    def update(self):
        """Call when forcing a refresh of the device."""
        # Reading the property (rather than last_level()) fetches value
        level = self._vantage_device.level
        _LOGGER.debug("Vantage ID: %d updated to %f",
                      self._vantage_device.id, level)

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        attr['Vantage Integration ID'] = self._vantage_device.id
        return attr