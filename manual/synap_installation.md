# Installing SyNAP

## Docker

Please follow these guidelines for Docker installation, but always consult the official [Docker documentation](https://docs.docker.com/get-docker/) for more details.

### Linux/Ubuntu

Install Docker with the following command:

```shell
apt-get install docker.io
```

To run Docker as a non-root user, execute these commands once after installing Docker (for more details, see the [Docker post-install guide](https://docs.docker.com/engine/install/linux-postinstall/)):

```shell
# Create the docker group if it doesn't already exist
sudo groupadd docker
# Add the current user "$USER" to the docker group
sudo usermod -aG docker $USER
```

### macOS - Docker

Install Docker on macOS using the `brew` package manager. If `brew` is not installed, follow the instructions on the [Homebrew website](https://brew.sh/).

```shell
brew install docker
```

**Important**: The Docker GUI is not free for commercial use on macOS. An alternative is `Colima`.

### macOS - Colima

`Colima` is a free alternative to Docker on macOS, suitable for container runtimes without a GUI. Install `Colima` and necessary tools with the following commands:

```shell
brew install colima
mkdir -p ~/.docker/cli-plugins
brew install docker-buildx
ln -sfn $(brew --prefix)/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
colima start --vm-type vz --mount-type virtiofs --cpu 4 --memory 8 --disk 80
```

To start Colima after a system restart:

```shell
colima start
```

For more information on using Colima, see this [guide](https://smallsharpsoftwaretools.com/tutorials/use-colima-to-run-docker-containers-on-macos/).

### Windows

Install Docker on Windows using WSL2 inside a Linux Virtual Machine. Docker running directly in Windows is not compatible with other VMs.

#### WSL2 Installation Steps

1. Open the *Windows PowerShell* as Administrator and run the command to install WSL2:

   ```shell
   > wsl --install
   ```

   Restart your computer when the installation is complete.

2. Install *Ubuntu-22.04* using *Windows PowerShell*:

   ```shell
   > wsl --install -d Ubuntu-22.04
   ```

3. Open *Windows Terminal*, select the *Ubuntu-22.04* distribution, and follow the Linux/Ubuntu installation instructions for Docker above.

For further information on WSL2, refer to Microsoft’s [WSL install guide](https://learn.microsoft.com/en-us/windows/wsl/install) and [WSL setup guide](https://learn.microsoft.com/en-us/windows/wsl/setup/environment).

## Installing SyNAP Tools

Before installing the SyNAP toolkit, ensure Docker is functioning by running the `hello-world` image:

```shell
$ docker run hello-world
```

If you see a welcome message from Docker, proceed with installing the toolkit. If not, check the Docker installation steps.

Download the SyNAP toolkit Docker image from the GitHub repository:

```shell
docker pull ghcr.io/synaptics-synap/toolkit:#SyNAP_Version#
```

The toolkit’s latest version is available [here](https://github.com/synaptics-synap/toolkit/pkgs/container/toolkit).

## Running SyNAP Tools

After installing Docker and the SyNAP toolkit, you can run the model conversion tool directly in a Docker container. To simplify repeated commands, create an alias:

```shell
alias synap='docker run -i --rm -u $(id -u):$(id -g) -v $HOME:$HOME -w $(pwd) ghcr.io/synaptics-synap/toolkit:#SyNAP_Version#'
```

This setup ensures that:

- The container runs interactively.
- The container is removed after exiting.
- The container runs with your user ID and group ID.
- Your home directory is mounted to the container.
- The working directory is set to your current directory.

To use the tool, type:

```shell
$ synap help
```

This command provides help and usage information for the toolkit. For detailed commands, run `synap COMMAND --help`.

**Important**: If you receive a *Permission Denied* error, revisit the Docker setup for non-root users as described above.