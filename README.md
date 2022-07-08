## Amazon AppStream 2.0 Linux Imaging Assistant

Amazon AppStream 2.0 provides secure, reliable, and scalable access to applications and non-persistent desktops from any location. Recently, an Amazon Linux 2 based offering was added. Unlike it's Windows counterparts, the linux version of AppStream does not include an image assistant. Instead admins are required to run a series of complex commands that are not well documented. The aim of this project is to ease the burden of creating images by providing a simple GUI and accelerate the creation process. 

![AppStream 2.0 Image Builder](https://github.com/aws-samples/appstream2-linux-imaging-assistant/blob/main/appstream2ImageBuilder.png)

## Executing the Assistant

There are two options when executing the Imaging Assistant. The first is to use the packaged binary, found on the releases tab. The binary's use is covered in the the [Image Assistant launch blog](LINK). The second option is to use the source code directly. In order to execute the code, you will need to have the required libraries readily available. The required libraries can be installed with the following commands:

```
sudo yum install -y python3-tkinter
pip3 install pygubu
sudo yum install -y git
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

