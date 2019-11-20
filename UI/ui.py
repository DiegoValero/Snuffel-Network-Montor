import hash
import ui_to_client as uitoc
import PySimpleGUI as sg

sg.ChangeLookAndFeel('Dark')

# Login screen
layout0 = [[sg.Image('./logo_2.png')],
           [sg.Text('Log in:')],
           [sg.Text('Username')],
           [sg.InputText(key='username')],
           [sg.Text('Password')],
           [sg.InputText(key='pass', password_char='*')],
           [sg.Button('Log in')]]

win1 = sg.Window('Snuffel administrative panel', layout0)
win2_active = False
win3_active = False
win4_active = False

# Main loop
while True:
    ev1, vals1 = win1.Read(timeout=100)
    if ev1 is None:
        break

    # Call the hash, check login.
    if ev1 == 'Log in':
        if vals1['username'] == 'admin':
            # If correct, go to main menu window
            if hash.compareHash(vals1['pass']):
                print('Login successful')
                win1.Hide()
                win1_active = True

                layout1 = [[sg.Image('./logo_2.png')],
                           [sg.Text('Menu:'), ],
                           [sg.Button('Add Website'), sg.Button('Manage desktops'), sg.Button('Mailing list')]]

                win1 = sg.Window('Manage administrators', layout1)

            # Try again
            else:
                layout0 = [[sg.Image('./logo_2.png')],
                           [sg.Text('Unknown username or password')],
                           [sg.Text('Log in:')],
                           [sg.Text('Username')],
                           [sg.InputText(key='username')],
                           [sg.Text('Password')],
                           [sg.InputText(key='pass', password_char='*')],
                           [sg.Button('Log in')]]
                win1.Close()
                win1 = sg.Window('Snuffel administrative panel', layout0)

        # Better luck next time
        else:
            layout0 = [[sg.Image('./logo_2.png')],
                       [sg.Text('Unknown username or password')],
                       [sg.Text('Log in:')],
                       [sg.Text('Username')],
                       [sg.InputText(key='username')],
                       [sg.Text('Password')],
                       [sg.InputText(key='pass', password_char='*')],
                       [sg.Button('Log in')]]
            win1.Close()
            win1 = sg.Window('Snuffel administrative panel', layout0)

    # Edit the list of prohibited websites
    if ev1 == 'Add Website' and not win2_active:
        win2_active = True
        win1.Hide()

        url = uitoc.request('Weblink')
        url_list = list(url.values())

        frame_layout = [[sg.Text('\n'.join(url_list))]]

        layout2 = [[sg.Text('Please fill in the url of the website to add or delete.')],
                   [sg.Text('URL:', size=(15, 1)), sg.InputText()],
                   [sg.Frame('Current Website List', frame_layout)],
                   [sg.Button('Submit'), sg.Button('Delete'), sg.Button('Exit')]]

        win2 = sg.Window('Add Website', layout2)

        while True:
            ev2, vals2 = win2.Read()

            if ev2 == 'Submit':
                uitoc.insert("URL", vals2[0], "")
                sg.Popup("Url successfully added to the list!\nReopen the window to refresh the list.")
            if ev2 == 'Delete':
                uitoc.drop("URL", vals2[0], "")
                sg.Popup("Url successfully deleted from the list!\nReopen the window to refresh the list.")
            if ev2 is None or ev2 == 'Exit':
                win2_active = False
                win2.Close()
                win1.UnHide()
                break

    # Remove or add desktops.
    if ev1 == 'Manage desktops' and not win3_active:
        win3_active = True
        win1.Hide()

        desktop = uitoc.request('Desktop')
        mac_list = list(desktop.values())
        id_list = list(desktop.keys())

        col1 = [[sg.Text('ID')],
                [sg.Text('\n'.join(str(x) for x in id_list))]]

        col2 = [[sg.Text('MAC')],
                [sg.Text('\n'.join(mac_list))]]

        frame_layout = [[sg.Column(col1), sg.Column(col2)]]

        layout3 = [[sg.Text('Please fill in the information of the new desktop')],
                   [sg.Text('ID:', size=(15, 1)), sg.InputText()],
                   [sg.Text('MAC address:', size=(15, 1)), sg.InputText()],
                   [sg.Frame('Current Desktop List', frame_layout)],
                   [sg.Button('Submit'), sg.Button('Delete'), sg.Button('Exit')]]

        win3 = sg.Window('Manage desktops', layout3)

        while True:
            ev3, vals3 = win3.Read()
            print(vals3[0], vals3[1])

            if ev3 == 'Submit':
                # moet nog fixen
                #uitoc.insert("Desktop", vals3[0], vals3[1])
                sg.Popup("Desktop successfully added to the list!\nReopen this window to refresh the list.")
            if ev3 == 'Delete':
                # moet nog fixen
                #uitoc.insert("Desktop", vals3[0], vals3[1])
                sg.Popup("Desktop successfully deleted from the list!\nReopen this window to refresh the list.")
            if ev3 is None or ev3 == 'Exit':
                win3_active = False
                win3.Close()
                win1.UnHide()
                break

    # Add or remove addresses in the mailing list
    if ev1 == 'Mailing list' and not win4_active:
        win4_active = True
        win1.Hide()

        emails = uitoc.request('Mail')
        mailAddresses = []
        name = []

        for address in emails:
            mailAddresses.append(address)

        for names in emails.values():
            name.append(names)

        if len(mailAddresses) == 0:
            mailAddresses.append('-')
        if len(mailAddresses) == 1:
            mailAddresses.append('-')
        if len(mailAddresses) == 2:
            mailAddresses.append('-')

        if len(name) == 0:
            name.append('-')
        if len(name) == 1:
            name.append('-')
        if len(name) == 2:
            name.append('-')

        layout4 = [[sg.Text('Current email addresses:')],
                   [sg.Text('1: ' + name[0])],
                   [sg.Text('Email: ' + mailAddresses[0])],
                   [sg.Text('')],
                   [sg.Text('2: ' + name[1])],
                   [sg.Text('Email: ' + mailAddresses[1])],
                   [sg.Text('')],
                   [sg.Text('3: ' + name[2])],
                   [sg.Text('Email: ' + mailAddresses[2])],
                   [sg.Text('')],
                   [sg.Text('Please fill in the information of the new email address')],
                   [sg.Text('Name:', size=(15, 1)), sg.InputText()],
                   [sg.Text('Email address:', size=(15, 1)), sg.InputText()],
                   [sg.Text('')],
                   [sg.Button('Submit'), sg.Button('Delete'), sg.Button('Exit')]]

        win4 = sg.Window('Mailing list', layout4)

        while True:
            ev4, vals4 = win4.Read()

            if ev4 == 'Submit':
                inserted = uitoc.insert("Mail", vals4[1], vals4[0])
                sg.Popup("E-mail address successfully added to the list!\nReopen this window to refresh the list.")
            if ev4 == 'Delete':
                uitoc.drop("Mail", vals4[1], vals4[0])
                sg.Popup("E-mail address successfully deleted from the list!\nReopen this window to refresh the list.")
            if ev4 is None or ev4 == 'Exit':
                win4_active = False
                win4.Close()
                win1.UnHide()
                break
