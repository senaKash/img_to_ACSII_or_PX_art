import pygame as pg
import cv2
import numpy as np

class ImgConverter:
    def __init__(self, path = 'imgs/1.jpg', font_size = 12, color_lvl = 16):
        pg.init()
        self.path = path
        self.COLOR_LVL = color_lvl
        self.image, self.gray_image = self.get_img()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.ASCII_CHARS = ' ############'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold = True)
        self.CHAR_STEP = int(font_size * 0.6)
        #self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]
        self.PALETTE, self.COLOR_COEFF = self.palette()
        
    def draw_converted_img(self):
        char_indices = self.gray_image // self.ASCII_COEFF
        color_indices = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indices[x, y])
                    self.surface.blit(self.PALETTE[char][color], (x, y))
                    #self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))
    
    def get_img(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        #rgb_image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2BGR)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2GRAY)
        return image, gray_image

    def palette(self):
        colors, color_coeff = np.linspace(0, 255, num = self.COLOR_LVL, dtype = int, retstep = True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, (300, 300), interpolation = cv2.INTER_AREA)
        #cv2.imshow('img', self.image)
        cv2.imshow('OpenCV', resized_cv2_image)
        
        
    def draw(self):
        self.surface.fill('black')
        self.draw_converted_img()
        #pg.surfarray.blit_array(self.surface, self.image) debug
        #cv2.imshow('img', self.image) 
        self.draw_cv2_image()

    def save_image(self):
        pygame_img = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_img)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite('out/outImg.jpg', cv2_img)
        
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
