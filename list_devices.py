import pygame.midi

pygame.midi.init()

print("🎹 Available MIDI Devices:\n")
for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    interf, name, is_input, is_output, opened = info
    io_type = "Output" if is_output else "Input"
    print(f"ID {i}: {name.decode()} | Type: {io_type}")

pygame.midi.quit()