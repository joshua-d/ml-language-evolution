import language_creation_7 as lang
import pygame
import math


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60


def show_info(screen):
    info_1 = pygame.image.load("info_1.png")
    info_2 = pygame.image.load("info_2.png")
    info_3 = pygame.image.load("info_3.png")
    info_4 = pygame.image.load("info_4.png")

    imgs = [info_1, info_2, info_3, info_4]
    current_img = 1

    screen.blit(info_1, (0, 0))
    pygame.display.flip()

    pressed = True
    while True:
        start_tick = pygame.time.get_ticks()
        pygame.event.get()

        if pygame.mouse.get_pressed()[0]:
            if not pressed:
                if current_img == 4:
                    return
                screen.blit(imgs[current_img], (0, 0))
                pygame.display.flip()
                current_img += 1
                pressed = True
        else:
            pressed = False

        pygame.time.wait(math.floor(1000 / FPS) - (pygame.time.get_ticks() - start_tick))


def render_text(screen, font, text, text_pos, color=(0, 0, 0)):
    sentence_text = font.render(text, True, color)
    text_rect = sentence_text.get_rect()
    text_rect.center = text_pos
    screen.blit(sentence_text, text_rect)


def slide_image(screen, image, pos_i, pos_f, speed):
    pos_i[0] += ((pos_f[0] - pos_i[0]) / speed)
    pos_i[1] += ((pos_f[1] - pos_i[1]) / speed)

    screen.blit(image, pos_i)


def pause():
    pressed = True
    while True:
        start_tick = pygame.time.get_ticks()
        pygame.event.get()

        if pygame.mouse.get_pressed()[0]:
            if not pressed:
                return
        else:
            pressed = False

        pygame.time.wait(math.floor(1000 / FPS) - (pygame.time.get_ticks() - start_tick))




def show_scene(screen, images, sentence, correct, subject, verb, noun, task, show_gen=True, show_buttons=True, show_task=False):

    speaker = [325, 250]
    receiver = [755, 250]
    bubble = [15, 80]
    text_pos = [315, 155]
    check_x = [540, 550]
    wheelbarrow = [520, 290]
    dirt = [640, 470]
    task_text_pos = [150, 400]

    carrot_give = [670, 300]
    carrot_receive = [450, 300]
    potato_give = [670, 350]
    potato_receive = [450, 350]

    carrot_plant_i = [660, 270]
    carrot_plant_f = [660, 400]
    potato_plant_i = [670, 330]
    potato_plant_f = [670, 460]

    font = pygame.font.Font('freesansbold.ttf', 28)
    gen_font = pygame.font.Font('freesansbold.ttf', 18)
    task_font = pygame.font.Font('freesansbold.ttf', 18)

    frame_time = 500
    for frame in range(frame_time):
        start_tick = pygame.time.get_ticks()
        pygame.event.get()

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[1] > 600:
                if pos[0] > 1100:
                    return 'go_back'
                elif pos[0] > 1000:
                    pause()
                elif pos[0] > 900:
                    return 'skip'
                elif pos[0] > 800:
                    return 'show_task'

        screen.blit(images['main_background'], (0, 0))

        if show_gen:
            render_text(screen, gen_font, "Generation: " + str(lang.get_generation()), [80, 670])

        if show_buttons:
            screen.blit(images['task_button'], (800, 600))
            screen.blit(images['skip_button'], (900, 600))
            screen.blit(images['pause_button'], (1000, 600))
            screen.blit(images['back_button'], (1100, 600))

        screen.blit(images['stickman'], speaker)
        screen.blit(images['stickman'], receiver)

        if frame > 60:
            screen.blit(images['bubble'], bubble)
            render_text(screen, font, sentence, text_pos)

            if show_task:
                render_text(screen, task_font, "(" + task[0] + " " + task[1] + " " + task[2] + ")", task_text_pos, (180, 180, 180))

        if frame > 180:
            if subject == 'i':
                if verb == "plant":
                    if noun == "carrots":
                        # I plant carrots
                        slide_image(screen, images['carrot'], carrot_give, carrot_receive, 10)
                    else:
                        # I plant potatoes
                        slide_image(screen, images['potato'], potato_give, potato_receive, 10)
                else:
                    if noun == "carrots":
                        # I harvest carrots
                        screen.blit(images['carrot_wheelbarrow'], wheelbarrow)
                    else:
                        # I harvest potatoes
                        screen.blit(images['potato_wheelbarrow'], wheelbarrow)
            else:
                if verb == "plant":
                    if noun == "carrots":
                        # You plant carrots
                        slide_image(screen, images['carrot'], carrot_plant_i, carrot_plant_f, 10)
                        screen.blit(images['dirt'], dirt)
                    else:
                        # You plant potatoes
                        slide_image(screen, images['potato'], potato_plant_i, potato_plant_f, 10)
                        screen.blit(images['dirt'], dirt)
                else:
                    if noun == "carrots":
                        # You harvest carrots
                        slide_image(screen, images['carrot'], carrot_plant_f, carrot_plant_i, 10)
                        screen.blit(images['dirt'], dirt)
                    else:
                        # You harvest potatoes
                        slide_image(screen, images['potato'], potato_plant_f, potato_plant_i, 10)
                        screen.blit(images['dirt'], dirt)

        if frame > 300:
            if correct:
                screen.blit(images['check'], check_x)
            else:
                screen.blit(images['x'], check_x)

        if frame > 480:
            screen.blit(images['main_background'], (0, 0))
            if show_gen:
                render_text(screen, gen_font, "Generation: " + str(lang.get_generation()), [80, 670])

            if show_buttons:
                screen.blit(images['task_button'], (800, 600))
                screen.blit(images['skip_button'], (900, 600))
                screen.blit(images['pause_button'], (1000, 600))
                screen.blit(images['back_button'], (1100, 600))

        pygame.display.flip()
        pygame.time.wait(math.floor(1000 / FPS) - (pygame.time.get_ticks() - start_tick))


def start_scratch(screen):

    lang.setup()

    main_background = pygame.image.load("main_background.png")
    stickman = pygame.image.load("stickman.png")
    carrot = pygame.image.load("carrot.png")
    potato = pygame.image.load("potato.png")
    carrot_wheelbarrow = pygame.image.load("carrot_wheelbarrow.png")
    potato_wheelbarrow = pygame.image.load("potato_wheelbarrow.png")
    bubble = pygame.image.load("bubble.png")
    check = pygame.image.load("check.png")
    x = pygame.image.load("x.png")
    dirt = pygame.image.load("dirt.png")
    task_button = pygame.image.load("task_button.png")
    pause_button = pygame.image.load("pause_button.png")
    skip_button = pygame.image.load("skip_button.png")
    back_button = pygame.image.load("back_button.png")

    images = {
        'main_background': main_background,
        'stickman': stickman,
        'carrot': carrot,
        'potato': potato,
        'carrot_wheelbarrow': carrot_wheelbarrow,
        'potato_wheelbarrow': potato_wheelbarrow,
        'bubble': bubble,
        'check': check,
        'x': x,
        'dirt': dirt,
        'task_button': task_button,
        'pause_button': pause_button,
        'skip_button': skip_button,
        'back_button': back_button
    }

    show_task = False
    while True:
        lang.do_round(lang.get_population(), lang.get_nenv_s(), lang.get_nenv_r())
        speaker = lang.get_population()[0]
        receiver = lang.get_population()[1]

        speaker.get_task()
        speaker.speak(receiver)

        if receiver.decision[0] == 1:
            subject = 'i'
        else:
            subject = 'you'
        if receiver.decision[2] == 1:
            verb = 'plant'
        else:
            verb = 'harvest'
        if receiver.decision[4] == 1:
            noun = 'carrots'
        else:
            noun = 'potatoes'

        task = [0, 0, 0]
            
        if speaker.task[0] == 1:
            task[0] = 'i'
        else:
            task[0] = 'you'
        if speaker.task[2] == 1:
            task[1] = 'plant'
        else:
            task[1] = 'harvest'
        if speaker.task[4] == 1:
            task[2] = 'carrots'
        else:
            task[2] = 'potatoes'

        correct = True
        for i in range(len(receiver.decision)):
            if receiver.decision[i] != speaker.task[i]:
                correct = False

        state = show_scene(screen, images, lang.translate_sentence(speaker.sentence), correct, subject, verb, noun, task, True, True, show_task)
        if state == 'go_back':
            return
        elif state == 'skip':
            for i in range(20):
                lang.do_round(lang.get_population(), lang.get_nenv_s(), lang.get_nenv_r())
        elif state == 'show_task':
            show_task = True


def start_view(screen):

    lang.setup()

    main_background = pygame.image.load("main_background.png")
    stickman = pygame.image.load("stickman.png")
    carrot = pygame.image.load("carrot.png")
    potato = pygame.image.load("potato.png")
    carrot_wheelbarrow = pygame.image.load("carrot_wheelbarrow.png")
    potato_wheelbarrow = pygame.image.load("potato_wheelbarrow.png")
    bubble = pygame.image.load("bubble.png")
    check = pygame.image.load("check.png")
    x = pygame.image.load("x.png")
    dirt = pygame.image.load("dirt.png")
    task_button = pygame.image.load("task_button.png")
    pause_button = pygame.image.load("pause_button.png")
    skip_button = pygame.image.load("skip_button.png")
    back_button = pygame.image.load("back_button.png")

    images = {
        'main_background': main_background,
        'stickman': stickman,
        'carrot': carrot,
        'potato': potato,
        'carrot_wheelbarrow': carrot_wheelbarrow,
        'potato_wheelbarrow': potato_wheelbarrow,
        'bubble': bubble,
        'check': check,
        'x': x,
        'dirt': dirt,
        'task_button': task_button,
        'pause_button': pause_button,
        'skip_button': skip_button,
        'back_button': back_button
    }

    speaker = lang.get_population()[0]
    receiver = lang.get_population()[1]

    speaker.speak_network = lang.get_nenv_s().import_network("speak_network.txt")
    receiver.receive_network = lang.get_nenv_r().import_network("receive_network.txt")

    show_task = False
    while True:

        speaker.get_task()
        speaker.speak(receiver)

        if receiver.decision[0] == 1:
            subject = 'i'
        else:
            subject = 'you'
        if receiver.decision[2] == 1:
            verb = 'plant'
        else:
            verb = 'harvest'
        if receiver.decision[4] == 1:
            noun = 'carrots'
        else:
            noun = 'potatoes'

        task = [0, 0, 0]

        if speaker.task[0] == 1:
            task[0] = 'i'
        else:
            task[0] = 'you'
        if speaker.task[2] == 1:
            task[1] = 'plant'
        else:
            task[1] = 'harvest'
        if speaker.task[4] == 1:
            task[2] = 'carrots'
        else:
            task[2] = 'potatoes'

        correct = True
        for i in range(len(receiver.decision)):
            if receiver.decision[i] != speaker.task[i]:
                correct = False

        state = show_scene(screen, images, lang.translate_sentence(speaker.sentence), correct, subject, verb, noun, task, False, True, show_task)
        if state == 'go_back':
            return
        elif state == 'show_task':
            show_task = True


def main_gui():
    pygame.init()
    pygame.display.set_caption("ML Language Evolution")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    start_img = pygame.image.load("start_screen.png")
    screen.blit(start_img, (0, 0))

    pressed = False
    running = True
    while running:
        start_tick = pygame.time.get_ticks()
        pygame.event.get()

        screen.blit(start_img, (0, 0))

        if pygame.mouse.get_pressed()[0]:
            if not pressed:
                pressed = True
                pos = pygame.mouse.get_pos()
                if  75 < pos[0] < 320:
                    if 325 < pos[1] < 410:
                        # Start
                        start_scratch(screen)
                    elif 440 < pos[1] < 525:
                        # View
                        start_view(screen)
                    elif 555 < pos[1] < 630:
                        # Info
                        show_info(screen)
                        screen.blit(start_img, (0, 0))
                print(pos)
        else:
            pressed = False


        pygame.display.flip()
        pygame.time.wait(math.floor(1000 / FPS) - (pygame.time.get_ticks() - start_tick))

main_gui()
