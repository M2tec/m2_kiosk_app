project('m2-kiosk-app',
        version: '0.0.1')

install_data('__init__.py', install_dir: get_option('datadir'))
install_data('m2-kiosk-app', install_dir: get_option('datadir'))
install_data('m2_util.py', install_dir: get_option('datadir'))
install_data('paypad.glade', install_dir: get_option('datadir'))
install_data('request_handlers.py', install_dir: get_option('datadir'))

install_data('m2_config.txt', install_dir: get_option('datadir'))
install_data('m2_config.json', install_dir: get_option('datadir'))
install_data('kiosk-app-test.py', install_dir: get_option('datadir'))

install_subdir('json-url-reduced', install_dir: get_option('datadir'))
install_subdir('payment_types', install_dir: get_option('datadir'))
install_subdir('payment_validators', install_dir: get_option('datadir'))
install_subdir('static', install_dir: get_option('datadir'))

#install_data('m2-kiosk-app.desktop', install_dir: 'etc/xdg/autostart')
install_data('m2-kiosk-app.desktop', install_dir: 'usr/share/applications')


install_subdir('DEBIAN', install_dir: '')
