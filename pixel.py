import pygame as pg
import cv2
import numpy as np
import pygame.gfxdraw

class ImgConverter:
    def __init__(self, pixel_size = 5, color_lvl = 32, inputPath = "например\\картинка.jpg", outPath = "например\\выходнаяКартинка.jpg"):
        pg.init()
        self.path = inputPath
        self.outPth = outPath
        self.PIXEL_SIZE = pixel_size
        self.COLOR_LVL = color_lvl
        self.image = self.get_img()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        
        
        self.PALETTE, self.COLOR_COEFF = self.palette()
        print("init correct")
        
    def draw_converted_img(self):
        
        color_indices = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                color_key = tuple(color_indices[x, y])
                if sum(color_key):
                    color = self.PALETTE[color_key]
                    pygame.gfxdraw.box(self.surface, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE), color)
    
    def get_img(self):
        self.cv2_image = cv2.imread(self.path)
        print(self.cv2_image)
        transposed_image = cv2.transpose(self.cv2_image)

        image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2BGR)

        return image

    def palette(self):
        colors, color_coeff = np.linspace(0, 255, num = self.COLOR_LVL, dtype = int, retstep = True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        
        return palette, color_coeff

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, (300, 700), interpolation = cv2.INTER_AREA)
        cv2.imshow('OpenCV', resized_cv2_image)
        
        
    def draw(self):
        self.surface.fill('black')
        self.draw_converted_img()
        self.draw_cv2_image()

    def save_image(self):
        pygame_img = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_img)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.outPth, cv2_img)
        
    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
                self.draw()
                pg.display.set_caption(str(self.clock.get_fps()))
                pg.display.flip()
                self.clock.tick()


if __name__ == '__main__':

    app = ImgConverter()
    app.run()

