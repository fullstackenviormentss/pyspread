#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2008 Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

"""
Cross-platform spreadsheet application.

See __init__.py for extensive docstring.

"""

# Patch for using with PyScripter thanks to Colin J. Williams
# If wx exists in sys,modules, we dont need to import wx version.
# wx is already imported if the PyScripter wx engine is used.

from sys import path, modules

try:
  modules['wx']
except KeyError:
    # End of patch
    
    # Select wx version 2.8 if possible

    try:
        import wxversion
        wxversion.select('2.8')
    except ImportError:
        pass

from wx import App
from wx import InitAllImageHandlers

DEBUG = False

# If pyspread is installed but run from a local dir
# the local libs are preferred.

path.insert(0, "..") 

class MainApplication(App):
    """Main application class for pyspread."""
    
    dimensions = (1, 1, 1) # Will be overridden anyways
    options = {}
    filename = None
    
    def OnInit(self):
        """Init class that is automatically run on __init__"""
        
        # Get command line options and arguments
        self.get_cmd_args()

        # Initialize the prerequisitions to construct the main window
        InitAllImageHandlers()

        # Main window creation
        from gui._main_window import MainWindow
        
        self.main_window = MainWindow(None, title="pyspread")
        
        ## Set dimensions
        
        ## Initialize file loading via event
        
        # Create GPG key if not present
        
        from _pyspread._interfaces import is_pyme_present
        
        if is_pyme_present():
            from _pyspread._interfaces import genkey
            genkey()
            
        # Show application window
        self.SetTopWindow(self.main_window)
        self.main_window.Show()

        #self.main_window.MainGrid.cursor = 0, 0

        # Load filename if provided
        if self.filename is not None:
            raise NotImplementedError
            ## TODO
            self.main_window.make_safe(self.filename)
            self.main_window.loadfile(self.filename)
        
        return True


    def get_cmd_args(self):
        """Returns command line arguments

        Created attributes
        ------------------
        
        options: dict
        \tCommand line options
        dimensions: Three tuple of Int
        \tGrid dimensions, default value (1,1,1).
        filename: String
        \tFile name that is loaded on start

        """

        from _pyspread._interfaces import Commandlineparser

        cmdp = Commandlineparser()
        self.options, self.filename = cmdp.parse()

        if self.filename is None:
            self.dimensions = self.options.dimensions


def __main__():
    """Compatibility hack"""
    
    pass


def main():
    """Parses command line and starts pyspread"""

    # Initialize main application
    app = MainApplication(0)

    app.MainLoop()


if __name__ == "__main__":
    if DEBUG:
        import cProfile
        cProfile.run('main()')
    else:
        main()