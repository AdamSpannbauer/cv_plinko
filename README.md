<p align='center'>
<h1><img src='readme/plinko_logo.png' width=20%> with OpenCV</h1>
</p>

Convert images/videos into plinko boards with Python + OpenCV.

## Example output

#### Static Images

The below output was created using the below command with [this input image](images/pyimage_combo.png).

```bash
 python -m cv_plinko -i images/pyimage_combo.png
```

<p align='center'>
<img src='readme/image_example.gif' width=70%>
</p>

#### Video/Webcam

The below output was created using the below command with a webcam.

```bash
 python -m cv_plinko -i 0
```

<p align='center'>
<img src='readme/video_example.gif' width=70%>
</p>
