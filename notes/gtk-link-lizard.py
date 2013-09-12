#!/usr/bin/python

# Code Name: gtk-link-lizard
# Created By: Jim Frize, <http://sonodrome.co.uk>
# Copyright (C) 2011 Jim Frize, <jim@sonodrome.co.uk>

# Licence: GTK Link Lizard is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>

# Version: 1.5
# Description: Simple GUI for storing and displaying web links

# This GUI will do away with synchronizing bookmarks between browsers, web links are stored in a regular text file which is found in your documents folder. GTK Link Lizard makes it easy to edit, swap or replace a list of clickable links. 

import pygtk
pygtk.require("2.0")  
import gtk
import sys
import re
import os

path = os.getenv("HOME")

class link_lizard():

    def __init__(self):

        self.load_main()

    #############
    # Load File #
    #############
    def load_file(self):

        # Look for links.txt in Documents folder
        try:
            self.text_file = open(path + "/Documents/gtk-link-lizard/links.txt","r")

        # If links.txt not found, load template from /usr/share/gtk-link-lizard
        except IOError:
            print "loading links.txt from /usr/share/gtk-link-lizard..."

            try:
                # Make gtk-link-lizard directory in Documents folder
                try:
                    os.mkdir(path + "/Documents/gtk-link-lizard")

                # Catch directory already exists exception 
                except OSError:
                    print "OSError: Directory: " + path + "/Documents/gtk-link-lizard already exists"

                # Open template and save it in Documents/gtk-link-lizard
                template = open("/usr/share/gtk-link-lizard/links.txt","r")
                read_template = template.read()
                self.text_file = open(path + "/Documents/gtk-link-lizard/links.txt","w")
                self.text_file.write(read_template)
                self.text_file = open(path + "/Documents/gtk-link-lizard/links.txt","r")

            # No template found, gtk-link-lizard probably not installed properly
            except IOError:
                print "IOError: links.txt not found, please check that gtk-link-lizard is installed properly"

    #################
    # Load main GUI #
    #################
    def load_main(self, data=None):
        # Create main window
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # Quit main function when window is destroyed
        self.main_window.connect("destroy", gtk.main_quit)
        self.main_window.set_size_request(600, 600)
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        self.main_window.set_opacity(0.9)
        self.main_window.set_title("GTK Link Lizard")
        self.main_window.set_keep_above(True)

        # Create scrolled window 
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        # Create placement boxes and dictionaries
        main_box = gtk.VBox(homogeneous=False)
        link_box = gtk.VBox(homogeneous=False)
        linkbutton = {}   
        label = {} 

        # Create edit button 
        edit_button = gtk.Button("Edit Links")
        edit_button.connect("clicked", self.load_edit)

        # Count number of lines in text file
        self.load_file()
        number_lines = len(self.text_file.readlines())

        # Reset counter and check through each line of text
        count = 0

        while(count < number_lines): 
            self.load_file()
            all_lines = self.text_file.readlines()
            current_line = all_lines[count]
            match = re.search("http://", current_line)
            match2 = re.search("https://", current_line)
            match3 = re.search("www.", current_line)

            # If http link is found, make a linkButton
            if match:               
                current_url = match.group()
                # Remove http://
                split_line = current_line.split("http://")
                
                if match3:
                    # Remove www. 
                    split_line = split_line[1].split("www.")

                linkbutton[count] = gtk.LinkButton(current_line, split_line[1])
                linkbutton[count].set_size_request(600, 30)
                link_box.pack_start(linkbutton[count], expand=False)

            # If https link is found, make a linkButton
            elif match2:
                current_url = match2.group()
                # Remove https://
                split_line = current_line.split("https://")

                if match3:
                    # Remove www.
                    split_line = split_line[1].split("www.")

                linkbutton[count] = gtk.LinkButton(current_line, split_line[1])
                linkbutton[count].set_size_request(600, 30)
                link_box.pack_start(linkbutton[count], expand=False)


            # If no link is found, add text as a label
            else:
                label[count] = gtk.Label(current_line)
                label[count].set_size_request(600, 20)
                link_box.pack_start(label[count], expand=False)

            count+=1

        # Add everything
        main_box.pack_start(edit_button, expand=False)
        scrolled_window.add_with_viewport(link_box)
        main_box.add(scrolled_window)
        self.main_window.add(main_box)
        self.main_window.show_all()

    #################
    # Load edit GUI #
    #################
    def load_edit(self, data=None):
        # Hide main window
        self.main_window.hide()
        # Create edit window
        self.edit_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # Return to main window when edit window is destroyed
        self.edit_window.connect("destroy", self.load_main)
        self.edit_window.set_size_request(600, 600)
        self.edit_window.set_position(gtk.WIN_POS_CENTER)
        self.edit_window.set_title("GTK Link Lizard (Editing Links)")

        # Create scrolled window 
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        # Create boxes for layout
        main_box = gtk.VBox(homogeneous=False)
        text_box = gtk.VBox(homogeneous=False)
        button_box = gtk.HBox(homogeneous=False)

        # Create buttons
        save_button = gtk.Button("Save")
        save_button.connect("clicked", self.save_edit)
        cancel_button = gtk.Button("Cancel")
        cancel_button.connect("clicked", self.cancel_edit)

        # Open file and display in text viewer
        self.load_file()
        all_text = self.text_file.read()
        text_buffer = gtk.TextBuffer()
        text_buffer.set_text(all_text)
        self.text_view = gtk.TextView(text_buffer)

        # Add everything
        button_box.add(save_button)
        button_box.add(cancel_button)
        text_box.add(self.text_view)
        scrolled_window.add_with_viewport(text_box)
        main_box.pack_start(button_box, expand=False)
        main_box.add(scrolled_window)
        self.edit_window.add(main_box)
        self.edit_window.show_all()

    #############
    # Save edit #
    #############
    def save_edit(self, data=None):
        save_buffer = self.text_view.get_buffer()
        save_text = save_buffer.get_text(save_buffer.get_start_iter(), save_buffer.get_end_iter())
        self.text_file = open(path + "/Documents/gtk-link-lizard/links.txt","w")
        self.text_file.write(save_text)
        self.edit_window.destroy()

    ###############
    # Cancel edit #
    ###############
    def cancel_edit(self, data=None):
        self.edit_window.destroy()

    #################
    # Main function #
    #################
    def main(self):
        gtk.main()

# Run main function when class is called
if __name__ == "__main__":
    new_link_lizard = link_lizard()
    new_link_lizard.main()
