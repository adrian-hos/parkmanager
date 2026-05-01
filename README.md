![Poza 1](https://github.com/adrian-hos/parkmanager/blob/main/imagini/fereastra_principala_blur.png "Fereastra Principala Blur")

# ParkManager

ParkManager este un program AI conceput pentru a simplifica gestionarea parcărilor private, fie că acestea aparțin unei companii, unei universități sau sunt utilizate în proprietăți rezidențiale. Programul, dezvoltat în limbajul de programare Python, utilizează două modele de inteligență artificială (AI) pentru a detecta și citi numerele de înmatriculare ale vehiculelor.

Acesta deschide automat o barieră pentru persoanele autorizate să intre în parcare. Prin eliminarea necesității telecomenzilor, care pot fi ușor pierdute sau descărcate, ParkManager aduce o soluție modernă și eficientă pentru gestionarea accesului auto în spații restricționate.

## Tehnologii utilizate

Pentru realizarea ParkManager, au fost utilizate următoarele instrumente și tehnologii:

1. **Python**, ca limbaj principal de programare.  
2. Modelul **YOLOv8** pentru detectarea numerelor de înmatriculare, ajustat prin *transfer learning*, împreună cu programul **Label Studio** și librăriile **Ultralytics** și **PyTorch** pentru pregătirea setului de date și antrenare.  
3. **Tesseract OCR 4** și **pytesseract** pentru recunoașterea caracterelor.  
4. **SQLite** și librăria **tempfile** pentru gestionarea bazei de date și a folderului temporar.  
5. **Qt 6**, **Qt Designer** și **PySide6** pentru dezvoltarea și implementarea interfeței grafice în Python.  
6. **OpenCV** pentru extragerea cadrelor de la o cameră video.  
7. **PySerial** pentru transmisia de date serială către barieră.  
8. **YAML** și **PyYAML** pentru stocarea setărilor în fișier.

![Poza 2](https://github.com/adrian-hos/parkmanager/blob/main/imagini/poza_bariera_fizica.jpg "Poza bariera fizica")