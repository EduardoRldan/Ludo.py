import tkinter as tk
import random
import winsound  # Para reproducir sonidos en Windows

class LudoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Ludo")

        # Dibujar el Tablero
        self.canvas = tk.Canvas(root, width=600, height=600, bg="lightgrey")  # Cambié el color de fondo
        self.canvas.pack()

        # Estado del juego
        self.positions = {"Player 1": 0, "Player 2": 0, "Player 3": 0, "Player 4": 0}
        self.turn = "Player 1"
        self.max_position = 56
        self.player_colors = {
            "Player 1": "red",
            "Player 2": "blue",
            "Player 3": "green",
            "Player 4": "yellow"
        }
        self.tokens = {}
        self.roll_count = 0

        # Interfaz del Usuario
        self.status_label = tk.Label(root, text="Turno del Jugador 1", font=("Arial", 16, "bold"), bg="lightgreen", width=30)  # Mejorada la apariencia
        self.status_label.pack()

        self.dice_label = tk.Label(root, text="Dado: ", font=("Arial", 14), bg="lightyellow", width=20)  # Mejorada la apariencia
        self.dice_label.pack()

        self.roll_button = tk.Button(root, text="Lanzar Dado", command=self.roll_dice, bg="lightblue", font=("Arial", 14), relief="raised", width=20)  # Mejorada la apariencia
        self.roll_button.pack()

        # Crear el tablero y fichas
        self.create_board()
        self.create_tokens()

    def create_board(self):
        """Dibuja el tablero de Ludo"""
        for i in range(15):
            self.canvas.create_line(40 * i, 0, 40 * i, 600, fill="black")
            self.canvas.create_line(0, 40 * i, 600, 40 * i, fill="black")

        # Zona central
        self.canvas.create_rectangle(240, 240, 360, 360, fill="gray")

        # Zonas iniciales
        self.canvas.create_rectangle(0, 0, 160, 160, fill="red")
        self.canvas.create_rectangle(0, 440, 160, 600, fill="blue")
        self.canvas.create_rectangle(440, 0, 600, 160, fill="green")
        self.canvas.create_rectangle(440, 440, 600, 600, fill="yellow")

    def create_tokens(self):
        """Crea las fichas de los jugadores en sus posiciones iniciales"""
        self.tokens["Player 1"] = self.canvas.create_oval(20, 20, 60, 60, fill="red")
        self.tokens["Player 2"] = self.canvas.create_oval(20, 500, 60, 540, fill="blue")
        self.tokens["Player 3"] = self.canvas.create_oval(500, 20, 540, 60, fill="green")
        self.tokens["Player 4"] = self.canvas.create_oval(500, 500, 540, 540, fill="yellow")

    def roll_dice(self):
        """Lanza el dado y mueve la ficha del jugador actual"""
        dice_value = random.randint(1, 6)
        self.dice_label.config(text=f"Dado: {dice_value}")

        # Verifica si el jugador necesita un 6 para salir
        if self.positions[self.turn] == 0 and dice_value != 6:
            self.status_label.config(text=f"{self.turn} necesita un 6 para salir")
            self.next_turn()
            return

        if dice_value == 6:
            self.roll_count += 1
            self.status_label.config(text=f"{self.turn} sacó un 6. Turno adicional")
        else:
            self.roll_count = 0

        self.move_token(dice_value)

    def move_token(self, steps):
        """Mueve la ficha del jugador actual según el resultado del dado"""
        current_pos = self.positions[self.turn]
        new_pos = current_pos + steps

        if new_pos > self.max_position:
            new_pos = current_pos

        # Capturar fichas de otros jugadores
        for player, pos in self.positions.items():
            if player != self.turn and new_pos == pos:
                self.positions[player] = 0
                self.update_token_position(player)
                self.play_capture_sound()  # Agregamos sonido para la captura

        self.positions[self.turn] = new_pos
        self.animate_token_move(self.turn, current_pos, new_pos)  # Llamamos la función de animación

        # Verificar si el jugador ha ganado
        if new_pos == self.max_position:
            self.status_label.config(text=f"¡{self.turn} ganó el juego! 🎉")
            self.roll_button.config(state=tk.DISABLED)
        else:
            if self.roll_count == 0:
                self.next_turn()

    def animate_token_move(self, player, start_pos, end_pos):
        """Función para animar el movimiento de la ficha"""
        start_x, start_y, _, _ = self.get_coordinates(start_pos, player)
        end_x, end_y, _, _ = self.get_coordinates(end_pos, player)
        
        steps = 20  # Definir la cantidad de pasos para la animación
        delta_x = (end_x - start_x) / steps
        delta_y = (end_y - start_y) / steps

        def move(step=0):
            if step <= steps:
                self.canvas.move(self.tokens[player], delta_x, delta_y)
                self.root.after(30, move, step + 1)  # Llama a la función cada 30ms para animar

        move()  # Inicia la animación

    def update_token_position(self, player):
        """Actualiza la posición visual de una ficha"""
        pos = self.positions[player]
        x1, y1, x2, y2 = self.get_coordinates(pos, player)
        self.canvas.coords(self.tokens[player], x1, y1, x2, y2)

    def get_coordinates(self, position, player):
        """Convierte una posición en coordenadas en el tablero"""
        if position == 0:
            return {
                "Player 1": (20, 20, 60, 60),
                "Player 2": (20, 500, 60, 540),
                "Player 3": (500, 20, 540, 60),
                "Player 4": (500, 500, 540, 540)
            }[player]

        row, col = divmod(position - 1, 7)
        x1 = col * 40 + 20
        y1 = row * 40 + 20
        x2 = x1 + 40
        y2 = y1 + 40
        return x1, y1, x2, y2

    def next_turn(self):
        """Pasa el turno al siguiente jugador"""
        if self.roll_count > 0:
            return  # Si sacó un 6, el turno se mantiene

        players = list(self.positions.keys())
        current_index = players.index(self.turn)
        next_index = (current_index + 1) % len(players)
        self.turn = players[next_index]
        self.status_label.config(text=f"Turno de {self.turn}")

    def play_capture_sound(self):
        """Reproduce el sonido de captura de ficha"""
        winsound.Beep(1000, 500)  # Tono de 1000Hz durante 500ms (ajustar según lo que desees)

if __name__ == "__main__":
    root = tk.Tk()
    game = LudoGame(root)
    root.mainloop()
