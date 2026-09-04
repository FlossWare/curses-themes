from curses_tui.geometry import Rect, SizeConstraints
from curses_tui.windows import HitRegion, Window, WindowManager


def test_rect_contains_move_resize_and_clamp():
    rect = Rect(8, 6, 20, 10)
    assert rect.contains(8, 6)
    assert not rect.contains(28, 16)
    assert rect.move(2, 3) == Rect(2, 3, 20, 10)
    assert rect.resize(30, 12) == Rect(8, 6, 30, 12)
    assert Rect(-5, -2, 30, 20).clamp(20, 10) == Rect(0, 0, 20, 10)


def test_constraints_enforce_min_and_max_size():
    constraints = SizeConstraints(min_width=10, min_height=4, max_width=30, max_height=12)
    assert constraints.constrain(2, 2) == (10, 4)
    assert constraints.constrain(40, 20) == (30, 12)
    assert constraints.constrain(20, 8) == (20, 8)


def test_window_hit_regions():
    window = Window("Test", Rect(10, 5, 20, 10))
    assert window.hit_test(12, 5) == HitRegion.TITLE
    assert window.hit_test(10, 5) == HitRegion.TOP_LEFT
    assert window.hit_test(29, 5) == HitRegion.TOP_RIGHT
    assert window.hit_test(10, 14) == HitRegion.BOTTOM_LEFT
    assert window.hit_test(29, 14) == HitRegion.BOTTOM_RIGHT
    assert window.hit_test(10, 9) == HitRegion.LEFT
    assert window.hit_test(29, 9) == HitRegion.RIGHT
    assert window.hit_test(15, 9) == HitRegion.BODY
    assert window.hit_test(2, 2) == HitRegion.NONE


def test_window_drag_moves_and_clamps_to_screen():
    window = Window("Test", Rect(10, 5, 20, 10))
    assert window.begin_interaction(14, 5)
    assert window.update_interaction(30, 20, 40, 30)
    assert window.rect == Rect(20, 20, 20, 10)
    window.update_interaction(100, 100, 40, 30)
    assert window.rect == Rect(20, 20, 20, 10)
    window.end_interaction()


def test_window_resize_respects_constraints():
    window = Window(
        "Test",
        Rect(10, 5, 20, 10),
        constraints=SizeConstraints(min_width=15, min_height=6, max_width=30, max_height=15),
    )
    assert window.begin_interaction(29, 14)
    assert window.update_interaction(40, 30, 80, 40)
    assert window.rect == Rect(10, 5, 30, 15)
    window.end_interaction()


def test_manager_focus_and_z_order():
    manager = WindowManager(100, 40)
    first = manager.add(Window("First", Rect(1, 1, 20, 8)))
    second = manager.add(Window("Second", Rect(5, 3, 20, 8)))
    assert manager.active is second
    assert manager.windows[-1] is second
    manager.focus(first)
    assert manager.active is first
    assert manager.windows[-1] is first


def test_manager_hit_test_prefers_topmost_and_mouse_focuses_it():
    manager = WindowManager(100, 40)
    first = manager.add(Window("First", Rect(1, 1, 30, 15)))
    second = manager.add(Window("Second", Rect(10, 5, 30, 15)))
    assert manager.hit_test(15, 8) is second
    assert manager.handle_mouse((15, 8, 0))
    assert manager.active is second
    assert first.focused is False


def test_manager_mouse_drag_and_release_moves_window():
    manager = WindowManager(80, 30)
    window = manager.add(Window("Test", Rect(10, 5, 20, 10)))
    pressed = getattr(__import__("curses"), "BUTTON1_PRESSED", 0)
    released = getattr(__import__("curses"), "BUTTON1_RELEASED", 0)
    assert pressed
    assert manager.handle_mouse((14, 5, pressed))
    assert window.interacting()
    motion = getattr(__import__("curses"), "REPORT_MOUSE_POSITION", 0)
    assert manager.handle_mouse((24, 10, motion))
    assert window.rect == Rect(20, 10, 20, 10)
    assert manager.handle_mouse((24, 10, released))
    assert not window.interacting()


def test_manager_mouse_click_body_starts_no_interaction_returns_true():
    manager = WindowManager(80, 30)
    window = manager.add(Window("Test", Rect(10, 5, 20, 10)))
    pressed = getattr(__import__("curses"), "BUTTON1_PRESSED", 0)
    # Clicking window body (15, 8) focuses window and returns True even though non-movable region
    assert manager.handle_mouse((15, 8, pressed))
    assert manager.active is window
    assert not window.interacting()


def test_manager_mouse_resize_and_release():
    manager = WindowManager(80, 40)
    window = manager.add(Window("Test", Rect(10, 5, 20, 10)))
    pressed = getattr(__import__("curses"), "BUTTON1_PRESSED", 0)
    released = getattr(__import__("curses"), "BUTTON1_RELEASED", 0)
    assert manager.handle_mouse((29, 14, pressed))
    assert manager.handle_mouse((39, 24, getattr(__import__("curses"), "REPORT_MOUSE_POSITION", 0)))
    assert window.rect.width == 30
    assert window.rect.height == 20
    assert manager.handle_mouse((39, 24, released))
    assert not window.interacting()


def test_manager_resize_screen_clamps_windows():
    manager = WindowManager(100, 40)
    window = manager.add(Window("Test", Rect(70, 30, 25, 12)))
    manager.resize_screen(80, 35)
    assert window.rect == Rect(55, 23, 25, 12)
