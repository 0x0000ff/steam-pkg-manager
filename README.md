# Preliminary Work on Package Management Tool(s) for Steamos
This is designed to work with other package managers in order to generate a launcher on steam with artwork- and possibly bundle control schemes as well.

Right now, it can run without root permissions. It will only support steam installations that have just one user.

## TODO

- ~~Add launcher data to steam~~
- ~~Add artwork to launcher~~
- Add controller mappings
- Get it working with a package manager
    - Make a service that runs the script when a new app is installled
    - Get the service to startup at boot-time
    - Add support for flatpak
    - Make a pull request for needed additions for the VDF library to get this to work

### Possible future developments
- Add support for other package managers/formats
- Support multiple users if there is a way to do it.