# Tic-Tac-Toe con MQTT y Mosquitto

## Descripción del programa

Este programa implementa el clásico juego de **Tic-Tac-Toe** (Tres en Raya) utilizando el protocolo **MQTT** con el broker **Mosquitto**. Permite que dos jugadores se conecten y jueguen en tiempo real, donde cada jugador puede hacer movimientos alternos. El estado del tablero se actualiza en ambas terminales gracias a la comunicación basada en mensajes que proporciona MQTT.

## Cómo funciona

El funcionamiento del juego se basa en el siguiente flujo:

1. **Conexión a Mosquitto**: El programa se conecta al broker MQTT en `localhost` y se suscribe al canal `tictactoe/game` para recibir los movimientos del oponente.
  
2. **Elección de símbolo**: Al iniciar el programa, cada jugador elige su símbolo (X o O). El jugador que elige X comienza primero.

3. **Turnos alternos**: Los jugadores alternan turnos para realizar sus movimientos. Solo se permite que el jugador activo realice un movimiento en su turno.

4. **Publicación de movimientos**: Cuando un jugador realiza un movimiento, el programa actualiza el estado del tablero localmente y envía el movimiento al broker MQTT. El formato del mensaje es `"{movimiento},{símbolo}"`, donde `movimiento` es el índice del espacio en el tablero (0-8) y `símbolo` es el símbolo del jugador.

5. **Recepción de movimientos**: El otro jugador recibe el mensaje a través de la función `on_message`, que actualiza su tablero y verifica si hay un ganador o si el juego ha terminado en empate.

6. **Finalización del juego**: El juego termina cuando un jugador gana (completa una fila, columna o diagonal) o si se llenan todos los espacios sin un ganador (empate). Se muestra el resultado en ambas terminales.

## Cómo jugar

Para jugar, sigue estos pasos:

1. Abre una terminal y ejecuta el siguiente comando `docker-compose up -d` para inciar el contenedor con mosquitto
2. En la misma terminal, ejecuta el comando `python3 tic_tac_toe.py` y abre otra terminal y ejecuta el mismo comando
3. En ambas terminales, se te pedira que selecciones un jugador (X / O), siempre empezará X a jugar
4. Por turnos, introduce la posición del tablero (0-8) en la que quieras colocar la ficha
5. El juego termina cuando hay una combinación ganadora o cuando el tablero está lleno y no se ha llegado a ninguna victoria (empate)
