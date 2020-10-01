A virtual clothing try on tool.

# About CMate
CMate is a virtual clothing try on tool. Given a profile image and a source image containing cloth, it applies the cloth to your profile image and let you see how does it look on you as if you were actually wearing it.<br>
It is a flask web application powered by deep learning.

### Features
- Supports all kinds of upper wear clothes for both men and women.
- Accurate cloth extraction and fitting.
- Simple, elegent and easy to use web app.

### How does it work ?
It works by extractng cloth from source image and fitting into your profile image.<br>
Under the hood, it uses two separate deep learning models:<br>
**Cloth segmentation model**: Custom Deeplab model to extract cloth from source image.<br>
**Pose estimator model**: Pretrained Openpose model used to locate shoulder points.<br>
Extracted cloth is blended into profile image based on shoulder location.

## Datasets
- Deepfashion2
- MPII Dataset

## Installation
Use docker image  or see installation.md.

## References
- Deeplab
- Openpose

## Contributing
Feel free to send pull requests on issue fixes or improvements.

## License
CMate is freely available for free non-commercial use under Apache License.

