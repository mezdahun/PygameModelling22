import pygame
import numpy as np
import sys

from pygmodw22 import support
from pygmodw22.agent import Agent

from math import atan2
import os
from datetime import datetime

root_abm_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Simulation:
    def __init__(self, N=10, T=1000, width=500, height=500, framerate=25, window_pad=30, with_visualization=True,
                 agent_radius=10):
        """
        Initializing the main simulation instance
        :param N: number of agents
        :param T: simulation time
        :param width: real width of environment (not window size)
        :param height: real height of environment (qnot window size)
        :param framerate: framerate of simulation
        :param window_pad: padding of the environment in simulation window in pixels
        :param with_visualization: turns visualization on or off. For large batch autmatic simulation should be off so
            that we can use a higher/maximal framerate.
        :param agent_radius: radius of the agents
        """
        # Arena parameters
        self.change_agent_colors = False
        self.WIDTH = width
        self.HEIGHT = height
        self.window_pad = window_pad

        # Simulation parameters
        self.N = N
        self.T = T
        self.t = 0
        self.with_visualization = with_visualization
        self.framerate_orig = framerate
        self.framerate = framerate
        self.is_paused = False
        self.show_zones = False
        self.physical_collision_avoidance = False

        # Agent parameters
        self.agent_radii = agent_radius

        # Initializing pygame
        pygame.init()

        # pygame related class attributes
        self.agents = pygame.sprite.Group()
        # Creating N agents in the environment
        self.create_agents()
        self.screen = pygame.display.set_mode([self.WIDTH + 2 * self.window_pad, self.HEIGHT + 2 * self.window_pad])
        self.clock = pygame.time.Clock()

    def draw_walls(self):
        """Drawing walls on the arena according to initialization, i.e. width, height and padding"""
        pygame.draw.line(self.screen, support.BLACK,
                         [self.window_pad, self.window_pad],
                         [self.window_pad, self.window_pad + self.HEIGHT])
        pygame.draw.line(self.screen, support.BLACK,
                         [self.window_pad, self.window_pad],
                         [self.window_pad + self.WIDTH, self.window_pad])
        pygame.draw.line(self.screen, support.BLACK,
                         [self.window_pad + self.WIDTH, self.window_pad],
                         [self.window_pad + self.WIDTH, self.window_pad + self.HEIGHT])
        pygame.draw.line(self.screen, support.BLACK,
                         [self.window_pad, self.window_pad + self.HEIGHT],
                         [self.window_pad + self.WIDTH, self.window_pad + self.HEIGHT])

    def draw_framerate(self):
        """Showing framerate, sim time and pause status on simulation windows"""
        tab_size = self.window_pad
        line_height = int(self.window_pad / 2)
        font = pygame.font.Font(None, line_height)
        status = [
            f"FPS: {self.framerate}, t = {self.t}/{self.T}",
        ]
        if self.is_paused:
            status.append("-Paused-")
        for i, stat_i in enumerate(status):
            text = font.render(stat_i, True, support.BLACK)
            self.screen.blit(text, (tab_size, i * line_height))

    def draw_agent_stats(self, font_size=15, spacing=0):
        """Showing agent information when paused"""
        # if self.is_paused:
        font = pygame.font.Font(None, font_size)
        for agent in self.agents:
            if agent.is_moved_with_cursor or agent.show_stats:
                status = [
                    f"ID: {agent.id}",
                    f"ori.: {agent.orientation:.2f}"
                ]
                for i, stat_i in enumerate(status):
                    text = font.render(stat_i, True, support.BLACK)
                    self.screen.blit(text, (agent.position[0] + 2 * agent.radius,
                                            agent.position[1] + 2 * agent.radius + i * (font_size + spacing)))

    def agent_agent_collision(self, agent1, agent2):
        """collision protocol called on any agent that has been collided with another one
        :param agent1, agent2: agents that collided"""
        # Updating all agents accordingly
        if not isinstance(agent2, list):
            agents2 = [agent2]
        else:
            agents2 = agent2

        for i, agent2 in enumerate(agents2):
            do_collision = True
            if do_collision:
                # overriding any mode with collision
                x1, y1 = agent1.position
                x2, y2 = agent2.position
                dx = x2 - x1
                dy = y2 - y1
                # calculating relative closed angle to agent2 orientation
                theta = (atan2(dy, dx) + agent2.orientation) % (np.pi * 2)

                # deciding on turning angle
                if 0 <= theta <= np.pi:
                    agent2.orientation -= np.pi / 8
                elif np.pi < theta <= 2 * np.pi:
                    agent2.orientation += np.pi / 8

                if agent2.velocity == 1:
                    agent2.velocity += 0.5
                else:
                    agent2.velocity = 1

    def add_new_agent(self, id, x, y, orient):
        """Adding a single new agent into agent sprites"""
        agent = Agent(
            id=id,
            radius=self.agent_radii,
            position=(x, y),
            orientation=orient,
            env_size=(self.WIDTH, self.HEIGHT),
            color=support.BLUE,
            window_pad=self.window_pad
        )
        self.agents.add(agent)

    def create_agents(self):
        """Creating agents according to how the simulation class was initialized"""
        for i in range(self.N):
            # allowing agents to overlap arena borders (maximum overlap is radius of patch)
            x = np.random.randint(self.window_pad - self.agent_radii, self.WIDTH + self.window_pad - self.agent_radii)
            y = np.random.randint(self.window_pad - self.agent_radii, self.HEIGHT + self.window_pad - self.agent_radii)

            # generating agent orientations
            orient = np.random.uniform(0, 2 * np.pi)

            self.add_new_agent(i, x, y, orient)

    def interact_with_event(self, events):
        """Carry out functionality according to user's interaction"""
        for event in events:
            # Exit if requested
            if event.type == pygame.QUIT:
                print('Bye bye!')
                pygame.quit()
                sys.exit()

            # Change orientation with mouse wheel
            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    event.y = 0
                for ag in self.agents:
                    ag.move_with_mouse(pygame.mouse.get_pos(), event.y, 1 - event.y)

            # Pause on Space
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused

            # Speed up on s and down on f. reset default framerate with d
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.framerate -= 5
                if self.framerate < 1:
                    self.framerate = 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.framerate += 5
                if self.framerate > 60:
                    self.framerate = 60

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.framerate = self.framerate_orig

            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                # Showing zone boundaries around agents
                self.show_zones = not self.show_zones

            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                # Showing agent orientations with fill colors
                self.change_agent_colors = not self.change_agent_colors
                for ag in self.agents:
                    ag.change_color_with_orientation = self.change_agent_colors

            # Continuous mouse events (move with cursor)
            if pygame.mouse.get_pressed()[0]:
                try:
                    for ag in self.agents:
                        ag.move_with_mouse(event.pos, 0, 0)

                except AttributeError:
                    for ag in self.agents:
                        ag.move_with_mouse(pygame.mouse.get_pos(), 0, 0)
            else:
                for ag in self.agents:
                    ag.is_moved_with_cursor = False
                    ag.draw_update()

    def draw_frame(self):
        """Drawing environment, agents and every other visualization in each timestep"""
        self.screen.fill(support.BACKGROUND)
        self.draw_walls()
        if self.show_zones:
            self.draw_agent_zones()
        self.agents.draw(self.screen)
        self.draw_framerate()
        self.draw_agent_stats()

    def draw_agent_zones(self):
        for agent in self.agents:
            image = pygame.Surface([self.WIDTH + self.window_pad, self.HEIGHT + self.window_pad])
            image.fill(support.BACKGROUND)
            image.set_colorkey(support.BACKGROUND)
            image.set_alpha(30)
            cx, cy, r = agent.position[0] + agent.radius, agent.position[1] + agent.radius, agent.r_att
            pygame.draw.circle(image, support.GREEN, (cx, cy), r, width=3)
            cx, cy, r = agent.position[0] + agent.radius, agent.position[1] + agent.radius, agent.r_rep
            pygame.draw.circle(image, support.RED, (cx, cy), r, width=3)
            cx, cy, r = agent.position[0] + agent.radius, agent.position[1] + agent.radius, agent.r_alg
            pygame.draw.circle(image, support.YELLOW, (cx, cy), r, width=3)
            self.screen.blit(image, (0, 0))

    def start(self):

        start_time = datetime.now()
        print(f"Running simulation start method!")

        print("Starting main simulation loop!")
        # Main Simulation loop until dedicated simulation time
        while self.t < self.T:

            events = pygame.event.get()
            # Carry out interaction according to user activity
            self.interact_with_event(events)

            if not self.is_paused:

                if self.physical_collision_avoidance:
                    # ------ AGENT-AGENT INTERACTION ------
                    # Check if any 2 agents has been collided and reflect them from each other if so
                    collision_group_aa = pygame.sprite.groupcollide(
                        self.agents,
                        self.agents,
                        False,
                        False,
                        within_group_collision
                    )
                    collided_agents = []
                    # Carry out agent-agent collisions and collecting collided agents for later (according to parameters
                    # such as ghost mode, or teleportation)
                    for agent1, agent2 in collision_group_aa.items():
                        self.agent_agent_collision(agent1, agent2)

                # Update agents according to current visible obstacles
                self.agents.update(self.agents)

                # move to next simulation timestep
                self.t += 1

            # Draw environment and agents
            if self.with_visualization:
                self.draw_frame()
                pygame.display.flip()

            # Moving time forward
            if self.t % 100 == 0 or self.t == 1:
                print(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')} t={self.t}")
                print(f"Simulation FPS: {self.clock.get_fps()}")
            self.clock.tick(self.framerate)

        end_time = datetime.now()
        print(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')} Total simulation time: ",
              (end_time - start_time).total_seconds())

        pygame.quit()


def within_group_collision(sprite1, sprite2):
    """Custom colllision check that omits collisions of sprite with itself. This way we can use group collision
    detect WITHIN a single group instead of between multiple groups"""
    if sprite1 != sprite2:
        return pygame.sprite.collide_circle(sprite1, sprite2)
    return False


def overlap(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)
