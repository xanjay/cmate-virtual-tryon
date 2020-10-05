<img src="https://github.com/xanjay/cmate-virtual-tryon/blob/master/src/flask_app/static/images/logo.png" height="200" /><br>
<img src="https://img.shields.io/docker/cloud/build/xanjay/cmate" /><br>
## About CMate
CMate is a virtual clothing try on tool. Given a profile image and a source image containing cloth, it applies the cloth to your profile image and let you see how does it look on you as if you were actually wearing it.<br>
It is a flask web application powered by deep learning.<br><br>
<img src="https://github.com/xanjay/cmate-virtual-tryon/blob/master/docs/cmate-demo.gif" height="300" /><br>
### Features
- Supports all kinds of upper wear clothes for both men and women.
- Accurate cloth extraction and fitting.
- Simple, elegent and easy to use web app.

### How does it work ?
It works by extractng cloth from source image and fitting into your profile image.<br>
Under the hood, it uses two separate deep learning models:<br>
**Cloth segmentation model**: Custom Deeplab model to extract cloth from source image.<br>
**Pose estimator model**: Pretrained Openpose body_25 model used to locate shoulder points.<br>
Extracted cloth is blended into profile image based on shoulder location.

## Dataset
- **Deepfashion2 Dataset**: used to train cloth segmentation model.

## Installation
Use [docker image](https://hub.docker.com/r/xanjay/cmate) OR see [installation.md](https://github.com/xanjay/cmate-virtual-tryon/blob/master/docs/installation.md).

## References
- Deeplab: https://github.com/tensorflow/models/tree/master/research/deeplab
- Deepfashion2 Dataset: https://github.com/switchablenorms/DeepFashion2
- Openpose: https://github.com/CMU-Perceptual-Computing-Lab/openpose

## Contributing
If you have any issue fixes or improvement changes. Fork this repo, make changes and submit pull request.

## License
CMate is freely available for free non-commercial use under [Apache License 2.0](https://github.com/xanjay/cmate-virtual-tryon/blob/master/LICENSE).