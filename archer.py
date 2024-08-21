from panda3d.core import Point3, Vec3, CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, CollisionSphere, AmbientLight, DirectionalLight
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
import sys

class ArcherGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Set up the environment
        self.setup_scene()
        
        # Load the archer and bow
        self.load_archer()
        
        # Load the target
        self.create_target()

        # Setup collision detection
        self.setup_collision()

        # Add controls
        self.accept("mouse1", self.shoot_arrow)
        self.accept("escape", sys.exit)

        # Game variables
        self.score = 0
        self.score_text = OnscreenText(text="Score: 0", pos=(-1.2, 0.9), scale=0.07, mayChange=True)

    def setup_scene(self):
        # Load environment model
        self.environment = self.loader.loadModel("models/environment")
        self.environment.reparentTo(self.render)
        self.environment.setScale(0.25, 0.25, 0.25)
        self.environment.setPos(-8, 42, 0)

        # Set up the camera
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(Point3(0, 0, 0))

        # Add lighting
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor((0.5, 0.5, 0.5, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))

        directional_light = DirectionalLight("directional_light")
        directional_light.setDirection(Vec3(-5, -5, -5))
        directional_light.setColor((0.7, 0.7, 0.7, 1))
        self.render.setLight(self.render.attachNewNode(directional_light))

    def load_archer(self):
        # Load archer model (using the panda model as a placeholder)
        self.archer = self.loader.loadModel("models/panda-model")
        self.archer.reparentTo(self.render)
        self.archer.setScale(0.005)
        self.archer.setPos(0, 0, 0)

        # Load bow model (using a simple box as a placeholder)
        self.bow = self.loader.loadModel("models/box")
        self.bow.reparentTo(self.archer)
        self.bow.setScale(0.2, 0.2, 0.5)
        self.bow.setPos(1, 1, 0.8)

    def create_target(self):
        # Load target model (using a simple box as a placeholder)
        self.target = self.loader.loadModel("models/box")
        self.target.reparentTo(self.render)
        self.target.setScale(1, 1, 1)
        self.target.setPos(0, 30, 0)

        # Add collision detection for the target
        target_coll_sphere = CollisionSphere(0, 0, 0, 1)
        target_coll_node = CollisionNode("target")
        target_coll_node.addSolid(target_coll_sphere)
        self.target_coll_np = self.target.attachNewNode(target_coll_node)

    def setup_collision(self):
        self.cTrav = CollisionTraverser()
        self.collision_handler = CollisionHandlerQueue()

        # Add the target's collision node to the traverser
        self.cTrav.addCollider(self.target_coll_np, self.collision_handler)

    def shoot_arrow(self):
        # Create an arrow (using a simple box as a placeholder)
        arrow = self.loader.loadModel("models/box")
        arrow.setScale(0.1, 0.5, 0.1)
        arrow.reparentTo(self.render)
        arrow.setPos(self.bow.getPos(self.render))

        # Move the arrow forward
        arrow_velocity = Vec3(0, 50, 0)
        arrow.setPythonTag("velocity", arrow_velocity)

        # Check for collisions
        self.taskMgr.add(self.move_arrow, "move_arrow", extraArgs=[arrow], appendTask=True)

    def move_arrow(self, arrow, task):
        # Move the arrow based on its velocity
        velocity = arrow.getPythonTag("velocity")
        arrow.setPos(arrow.getPos() + velocity * globalClock.getDt())

        # Check for collision with the target
        self.cTrav.traverse(self.render)
        for entry in self.collision_handler.getEntries():
            if entry.getIntoNode().getName() == "target":
                self.target_hit(arrow)
                return task.done

        # Remove the arrow if it goes out of bounds
        if arrow.getY() > 50:
            arrow.removeNode()
            return task.done

        return task.cont

    def target_hit(self, arrow):
        self.score += 1
        self.score_text.setText(f"Score: {self.score}")
        arrow.removeNode()
        print("Hit!")

game = ArcherGame()
game.run()
