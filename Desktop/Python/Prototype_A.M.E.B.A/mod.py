import pygame

pygame.font.init()

class Text():
    def __init__(self,master, text, x, y, font_size=36, font= None,color = (0,0,0)) -> None:
        """

        :param master: Экран для размещения
        :param text: Текст
        :param x: Координата x
        :param y: Координата y
        :param font_size: Размер шрифта
        :param font: Шрифт
        :param color: Цвет
        """
        font = pygame.font.Font(font, font_size)
        label = font.render(str(text),True, color)
        label_rect = label.get_rect()
        label_rect.midtop =(x,y)

        master.blit(label, label_rect)


class Bar():
    def __init__(self,master,height,width,x,y,src,fg,bg) -> None:
        """

        :param master: Экран для размещения
        :param height: Высота
        :param width: Широта
        :param x: Координата x
        :param y: Координата y
        :param src: Заполнение
        :param fg:  цвет внутреннего прямоугольника
        :param bg: Цвет внешнего прямоугольника
        """
        if src < 0:
            src = 0
            
        baсkground = pygame.rect.Rect(x, y, width, height)
        fonground = pygame.rect.Rect(x, y, src, height)
        pygame.draw.rect(master, bg, baсkground)
        pygame.draw.rect(master, fg, fonground)
        
class Button():
    def __init__(self,master, x, y, text,  pass_img, active_img, command, color = (0,0,0)):
        """

        :param master: Экран для размещения
        :param x: Координата x
        :param y: Координата y
        :param text: Текст
        :param pass_img: изображение кнопки
        :param active_img: Изображение при наведении
        :param command: комаанда вызывается при нажатии
        :param color: Цвет текста
        """
        on_pressed = False
        rect = pass_img.get_rect()
        rect.x = x
        rect.y = y



        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        
      
        if pressed[0]:
            if rect.collidepoint(pos[0], pos[1]):
                on_pressed = True


        if on_pressed:
            command()
            on_pressed = False

        if rect.collidepoint(pos[0], pos[1]):
            master.blit(active_img,(x,y))
        else:
            master.blit(pass_img,(x,y))         
        Text(master = master,
        text = text,
        x = (rect.x + rect.width//2) -   20 ,
        y = rect.y + rect.height//2,
        font_size = 25,
        color = color
        )
