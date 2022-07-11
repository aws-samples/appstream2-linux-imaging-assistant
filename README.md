## Amazon AppStream 2.0 Linux Imaging Assistant

Amazon AppStream 2.0 provides secure, reliable and scalable access to applications and non-persistent desktops from any location. At re:Invent 2021, AppStream announced the availability of Amazon Linux 2 images. With this release, users can now stream Linux applications and desktops. These images use a new set of, on instance, CLI tools to create an application catalog and capture images. This project provides a graphical experience similar to Windows based AppStream images that sits on top of the provided CLI.

![AppStream 2.0 Image Builder](https://github.com/aws-samples/appstream2-linux-imaging-assistant/blob/main/appstream2ImageBuilder.png)

## Running the Assistant

For administrators that simply want to use the tool, a pre-packaged binary is provided. The binary can be downloaded to an AppStream 2.0 Image Builder instance and run directly. This pattern is outlined in the launch announcement on the Desktop and Application Streaming Blog [Image Assistant launch blog](LINK).

## Install from Source

1. Connect to an Amazon Linux based AppStream Image Builder
2. Click Applications in the top left and then click the Terminal icon
3. Clone this git repository 
4. CD to the repo folder
5. Install the prerequisites using the following commands
```
sudo yum install -y python3-tkinter git
pip3 install -r ./source/requirements.txt
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.