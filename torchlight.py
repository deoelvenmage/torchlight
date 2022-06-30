# Important consts: Square size and maze size. Screen size = maze size * square size.
# Alternatively, only grid-square-size, and currentMapSize is a member/global variable that gets updated with every level, getting bigger

# Imports
import arcade
import random

# Constants
SPRITE_SIZE = 16
MAZE_SIZE = 20
SCALING = 2.0 # I predict unpredictable behavior if this does nt even divide both sprite and maze size
SCALING_INT = int(SCALING)
SCREEN_WIDTH = SPRITE_SIZE * MAZE_SIZE * SCALING_INT
SCREEN_HEIGHT = SPRITE_SIZE * MAZE_SIZE * SCALING_INT
SCREEN_TITLE = "Torchlight"

class Torchlight(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the top left, must find exit
    Player can move anywhere, but not off screen
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """
        Initialize the game
        """
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.wall_list = arcade.SpriteList()
        # self.fog_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.paused = False
    
    def setup(self): # TODO big setup in here; call generateMaze with MazeSize. Or just start it right now. Nah, make generator.
        """
        Get the game ready to play
        """

        # Set the background color
        arcade.set_background_color((219, 168, 140))

        # Set up the player
        self.player = arcade.Sprite("./images/skull_v2_1.png", SCALING)
        self.player.top = self.height
        self.player.left = 0
        self.all_sprites.append(self.player)

        self.end_tile = arcade.Sprite("./images/end_tile.png", SCALING)
        self.end_tile.left = 0
        self.end_tile.top = 0
        self.all_sprites.append(self.end_tile)        

        # Set up the maze
        def create_maze():
            """
            Credit for maze generation technique goes to github.com/ChickenSlayer3000/Random-Maze-Generator
            Modified some variables for readability; others I decided not to mess with
            For deciphering, I understand scr and scc to be StartingCellRow and StartingCellColumn;
            similar with Current and End.           
            """

            cell_size = SPRITE_SIZE #pixels; todo remove if not needed
            ms = MAZE_SIZE # rows and columns
            visited_cells = []
            walls = []
            revisited_cells = []

            map = [['Blocked' for _ in range(ms)]for _ in range(ms)]

            def create(): # TODO changing this for now
                for row in range(ms):
                    for col in range(ms):
                        if map[row][col] == 'Open':
                            pass
                            # Do nothing for now; background has us covered here; may want to change this later when we add more hazards like pits
                        elif map[row][col] == 'Blocked':
                            sprite = arcade.Sprite("./images/wall_tile.png", SCALING)

                            x = col * SPRITE_SIZE * SCALING_INT
                            y = row * SPRITE_SIZE * SCALING_INT

                            sprite.left = x
                            sprite.top = y
                            self.wall_list.append(sprite)
                            self.all_sprites.append(sprite)

            """Idea for a fixed create function. "Build" might be a better name too; wait hang on it might be working"""
            # def create():
            #     for item in revisited_cells:


            def check_neighbours(ccr, ccc):
                neighbours = [[ccr, ccc-1, ccr-1, ccc-2, ccr, ccc-2, ccr+1, ccc-2, ccr-1, ccc-1, ccr+1, ccc-1], #left
                            [ccr, ccc+1, ccr-1, ccc+2, ccr, ccc+2, ccr+1, ccc+2, ccr-1, ccc+1, ccr+1, ccc+1], #right
                            [ccr-1, ccc, ccr-2, ccc-1, ccr-2, ccc, ccr-2, ccc+1, ccr-1, ccc-1, ccr-1, ccc+1], #top
                            [ccr+1, ccc, ccr+2, ccc-1, ccr+2, ccc, ccr+2, ccc+1, ccr+1, ccc-1, ccr+1, ccc+1]] #bottom
                visitable_neighbours = []           
                for i in neighbours:                                                                        #find neighbours to visit
                    if i[0] > 0 and i[0] < (ms-1) and i[1] > 0 and i[1] < (ms-1):
                        if map[i[2]][i[3]] == 'Open' or map[i[4]][i[5]] == 'Open' or map[i[6]][i[7]] == 'Open' or map[i[8]][i[9]] == 'Open' or map[i[10]][i[11]] == 'Open':
                            walls.append(i[0:2])                                                                                               
                        else:
                            visitable_neighbours.append(i[0:2])
                return visitable_neighbours

            #StartingPoint

            scr = random.randint(1, ms)
            scc = random.randint(1, ms)

            # Change player position
            self.player.left = scc * SPRITE_SIZE * SCALING_INT
            self.player.top = scr * SPRITE_SIZE * SCALING_INT

            ccr, ccc = scr, scc

            map[ccr][ccc] = 'Open'
            finished = False
            while not finished:
                visitable_neighbours = check_neighbours(ccr, ccc)
                if len(visitable_neighbours) != 0:
                    d = random.randint(1, len(visitable_neighbours))-1
                    ncr, ncc = visitable_neighbours[d]
                    map[ncr][ncc] = 'Open'
                    visited_cells.append([ncr, ncc])
                    ccr, ccc = ncr, ncc
                if len(visitable_neighbours) == 0:
                    try:
                        ccr, ccc = visited_cells.pop()
                        revisited_cells.append([ccr, ccc])
                    except:
                        finished = True

            create()
            end = random.randint(1, len(revisited_cells))-1
            ecr = revisited_cells[end][0]
            ecc = revisited_cells[end][1]

            # change end tile position
            self.end_tile.left = ecc * SPRITE_SIZE * SCALING_INT
            self.end_tile.top = ecr * SPRITE_SIZE * SCALING_INT
        
        create_maze()

        # self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        # TODO set up PhysicEngine, which will just prevent the player from going through walls. May need to look at hitboxAlgorithm parameter
    
    def on_key_press(self, symbol, modifiers): #Make this call update (turn_update?) with a parameter of 'command'; we'll use this over on_update
        """Handle user keyboard input
        Q: Quit the game
        P: Pause/Unpause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 5

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int): #This is removable cause we dodn't do key release
        """Undo movement vectors when movement keys are released

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If paused, do nothing
    
        Arguments:
            delta_time {float} -- Time since the last update
        """
    
        # If paused, don't update anything
        if self.paused:
            return
        
        # End the game if you reach the end
        if self.player.collides_with_sprite(self.end_tile):
            arcade.close_window() 
    
        # Update everything
        self.all_sprites.update()
    
        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0
    
    def on_draw(self):
        """Draw all game objects
        """
        arcade.start_render()
        self.all_sprites.draw()
            
def main():
    """ Main function """
    window = Torchlight(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()