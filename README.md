# ROBO HAND

A brief description of what this project does and who it's for


## Authors

- [@paolalomeli11](https://github.com/paolalomeli11)


## Materiales
Hardware:

    •	Raspberry Pi 4 Model B Rev 1.1 (1)

    •	Servomotores (5)

    •	Modulo PCA9685 16 canales (1)

    •	Cámara (webcam USB) (1)

    •	Cables y fuente de alimentación

    •	Mano robótica (1)



## Configuración
1.	**Ensamblar mano robótica.** Para ensamblar la mano robótica se siguieron las instrucciones descritas en el siguiente enlace: https://www.instructables.com/3D-Printed-Robotic-Arm-2/
 
       ![image](https://github.com/user-attachments/assets/666e7fb9-c128-49fb-be4e-742fbb2fda42)
  
       Ilustración 1 Mano robótica



2.	**Realizar conexiones.** Una vez ensamblada la mano robótica, se procedió a realizar la conexión entre el modulo PCA9685 y la Raspberry Pi como se muestra en la ilustración 2. Además, se realiza la conexión de los servomotores al módulo PCA9685, debiendo estar los servomotores conectados en el orden y posición especificado en la ilustración 3.

       ![Ilustración 2 Conexión entre Raspberry Pi y modulo PCA9685](https://github.com/user-attachments/assets/44db6f3e-1f03-4103-aab0-2df811b43dee)

       Ilustración 2 Conexión entre Raspberry Pi y modulo PCA9685

      ![image](https://github.com/user-attachments/assets/69eb9b83-15d4-489e-aca8-057d7c6a304f)

      Ilustración 3 Conexión de servomotores



3.	**Correr script.** Una vez teniendo todas las dependencias instaladas y todo configurado correctamente correr el script “start_hand_tracking.py”.

      ![image](https://github.com/user-attachments/assets/a8509e0a-a2cd-41a5-acd8-7144a2801cfe)

