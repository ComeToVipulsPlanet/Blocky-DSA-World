"""
Visualizer Canvas Module — 3D-Style Blocky DSA World
---------------------------------------------------
Renders an isometric, Roblox-inspired 3D blocky visual playground on a pure Tkinter Canvas.
Features:
- Procedural 3D voxel terrain, drifting clouds, voxel sun, blocky trees.
- Original blocky coder avatar with interactive speech bubble.
- 3D isometric blocks with top studs, multi-face shading, and bold labels.
- Vertical Stack tower with dynamic height slots and floating animated TOP pointer.
- Horizontal Queue conveyor belt runway with chevrons, FRONT, and REAR pointers.
- Frame-by-frame animations using `canvas.after()` (never blocking the main GUI thread).
- Synchronization strictly driven by actual Stack and Queue models.
"""

import math
import tkinter as tk
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.stack import Stack
from src.queue_linked_list import Queue
from src.bst import BinarySearchTree, Node


# Color palettes for 3D toy blocks (front face, top face highlight, side shadow, text)
BLOCK_PALETTES = [
    {"front": "#E74C3C", "top": "#F1948A", "side": "#B03A2E", "text": "#FFFFFF"},  # Ruby Red
    {"front": "#3498DB", "top": "#85C1E9", "side": "#21618C", "text": "#FFFFFF"},  # Ocean Blue
    {"front": "#2ECC71", "top": "#82E0AA", "side": "#1E8449", "text": "#FFFFFF"},  # Emerald Green
    {"front": "#F39C12", "top": "#F8C471", "side": "#B9770E", "text": "#FFFFFF"},  # Gold Amber
    {"front": "#9B59B6", "top": "#BB8FCE", "side": "#6C3483", "text": "#FFFFFF"},  # Amethyst Purple
    {"front": "#00BCD4", "top": "#80DEEA", "side": "#00838F", "text": "#FFFFFF"},  # Neon Cyan
    {"front": "#E91E63", "top": "#F48FB1", "side": "#AD1457", "text": "#FFFFFF"},  # Coral Pink
]


class VisualizerCanvas(tk.Canvas):
    """
    Tkinter Canvas widget rendering the 3D-style DSA Blocky World.
    """

    def __init__(self, parent: tk.Widget, **kwargs):
        # Default sky blue background
        kwargs.setdefault("bg", "#6BB5EE")
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(parent, **kwargs)

        self.stack_ref: Optional[Stack] = None
        self.queue_ref: Optional[Queue] = None
        self.bst_ref: Optional[BinarySearchTree] = None
        self.mode: str = "STACK_QUEUE"  # "STACK_QUEUE" or "BST"
        self.highlighted_bst_node: Optional[int] = None
        self.highlighted_bst_path: List[int] = []
        self.bst_beam_highlight: Optional[Tuple[int, int]] = None
        self.bst_visited_nodes: List[int] = []
        self.bst_duplicate_node: Optional[int] = None

        # Animation state guards
        self.is_animating: bool = False
        self._cloud_after_id: Optional[str] = None
        self._anim_after_id: Optional[str] = None
        self.on_animation_finished: Optional[Callable[[], None]] = None

        # Cloud positions for gentle drift
        self.clouds: List[Dict[str, float]] = [
            {"x": 60, "y": 45, "speed": 0.35, "width": 110},
            {"x": 380, "y": 70, "speed": 0.25, "width": 130},
            {"x": 720, "y": 35, "speed": 0.40, "width": 95},
        ]

        # Avatar state & speech
        self.avatar_speech: str = "Welcome to Blocky DSA World! Push a block or enqueue an item to begin."
        self.bob_phase: float = 0.0

        # Highlights for Peek/Front/Rear
        self.highlighted_stack_idx: Optional[int] = None
        self.highlighted_queue_idx: Optional[int] = None

        # Bind resize and cloud loop
        self.bind("<Configure>", self._on_resize)
        self._cloud_drift_loop()

    def destroy(self) -> None:
        """Cancel scheduled after callbacks cleanly before destruction."""
        if self._cloud_after_id:
            try:
                self.after_cancel(self._cloud_after_id)
            except Exception:
                pass
            self._cloud_after_id = None
        if self._anim_after_id:
            try:
                self.after_cancel(self._anim_after_id)
            except Exception:
                pass
            self._anim_after_id = None
        super().destroy()

    def set_data_sources(self, stack: Stack, queue: Queue) -> None:
        """Bind live Stack and Queue models."""
        self.stack_ref = stack
        self.queue_ref = queue
        self.redraw()

    def set_bst_source(self, bst: BinarySearchTree) -> None:
        """Bind live Binary Search Tree model."""
        self.bst_ref = bst
        if self.mode == "BST":
            self.redraw()

    def set_mode(self, mode: str) -> None:
        """Switch visualizer view mode: 'STACK_QUEUE' or 'BST'."""
        self.mode = mode
        self.redraw()

    def set_speech(self, message: str) -> None:
        """Update avatar speech bubble message."""
        self.avatar_speech = message
        self.redraw()

    # -------------------------------------------------------------------------
    # RESIZING & BACKGROUND LOOPS
    # -------------------------------------------------------------------------
    def _on_resize(self, event) -> None:
        if not self.is_animating:
            self.redraw()

    def _cloud_drift_loop(self) -> None:
        if not self.winfo_exists():
            return

        width = self.winfo_width() or 900
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > width + 100:
                cloud["x"] = -150

        # Avatar subtle idle breathing animation
        self.bob_phase = (self.bob_phase + 0.1) % (2 * math.pi)

        if not self.is_animating:
            self.redraw()

        # Schedule next subtle drift tick (every 80ms)
        self._cloud_after_id = self.after(80, self._cloud_drift_loop)

    # -------------------------------------------------------------------------
    # PROCEDURAL RENDERING PIPELINE
    # -------------------------------------------------------------------------
    def redraw(self) -> None:
        """Completely redraws all static and dynamic elements on the Canvas."""
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()

        if width < 100 or height < 100:
            width = 850
            height = 550

        self._draw_sky_and_sun(width, height)
        self._draw_clouds()
        self._draw_voxel_landscape(width, height)
        self._draw_avatar_mascot(width, height)

        if self.mode == "BST":
            if self.bst_ref:
                self._draw_bst_platform(width, height)
        else:
            if self.stack_ref:
                self._draw_stack_platform(width, height)

            if self.queue_ref:
                self._draw_queue_platform(width, height)

    def _draw_sky_and_sun(self, width: int, height: int) -> None:
        # Sky gradient simulation using stacked horizontal color bands
        sky_colors = ["#4A90E2", "#5DADE2", "#76D7C4", "#A3E4D7"]
        band_h = height // len(sky_colors)
        for i, color in enumerate(sky_colors):
            y1 = i * band_h
            y2 = height if i == len(sky_colors) - 1 else (i + 1) * band_h
            self.create_rectangle(0, y1, width, y2, fill=color, outline="")

        # 3D Voxel Sun in top right corner
        sun_x = width - 110
        sun_y = 55
        # Outer glow
        self.create_oval(sun_x - 35, sun_y - 35, sun_x + 35, sun_y + 35, fill="#FFF9C4", outline="")
        # 3D Yellow Sun Cube
        self._draw_3d_cube(sun_x - 20, sun_y - 20, 40, 40, 10, 8, "#F1C40F", "#F9E79F", "#D4AC0D")
        # Sun smiley face
        self.create_oval(sun_x - 8, sun_y - 5, sun_x - 4, sun_y - 1, fill="#7D6608", outline="")
        self.create_oval(sun_x + 4, sun_y - 5, sun_x + 8, sun_y - 1, fill="#7D6608", outline="")
        self.create_arc(sun_x - 9, sun_y - 3, sun_x + 9, sun_y + 9, start=190, extent=160, style=tk.ARC, width=2, outline="#7D6608")

    def _draw_clouds(self) -> None:
        for cloud in self.clouds:
            cx = cloud["x"]
            cy = cloud["y"]
            cw = cloud["width"]
            # Multi-block voxel cloud
            self._draw_3d_cube(cx, cy, cw * 0.6, 22, 10, 8, "#FFFFFF", "#FDFEFE", "#BDC3C7", studs=False)
            self._draw_3d_cube(cx + 25, cy - 12, cw * 0.5, 24, 10, 8, "#FFFFFF", "#FFFFFF", "#D5D8DC", studs=False)
            self._draw_3d_cube(cx + 50, cy + 4, cw * 0.45, 18, 8, 6, "#F2F4F4", "#FFFFFF", "#BDC3C7", studs=False)

    def _draw_voxel_landscape(self, width: int, height: int) -> None:
        # Ground split: bottom 38% of canvas is voxel ground
        ground_y = int(height * 0.62)

        # Green voxel grass top platform
        self.create_rectangle(0, ground_y, width, ground_y + 24, fill="#2ECC71", outline="#27AE60", width=2)
        # Dirt and rock cliff layer below
        self.create_rectangle(0, ground_y + 24, width, height, fill="#795548", outline="#5D4037", width=2)

        # Grid lines on grass for voxel floor feeling
        for gx in range(0, width, 40):
            self.create_line(gx, ground_y, gx, ground_y + 24, fill="#27AE60", width=1)
            # Dirt rock pattern
            if (gx // 40) % 2 == 0:
                self.create_rectangle(gx + 8, ground_y + 35, gx + 28, ground_y + 55, fill="#6D4C41", outline="#4E342E")

        # Decorative Voxel Pine Trees on left and right margins
        self._draw_voxel_tree(35, ground_y)
        self._draw_voxel_tree(width - 55, ground_y)

    def _draw_voxel_tree(self, root_x: int, ground_y: int) -> None:
        # Brown Trunk blocks
        trunk_w = 16
        trunk_h = 36
        self._draw_3d_cube(root_x - trunk_w // 2, ground_y - trunk_h, trunk_w, trunk_h, 6, 5, "#8D6E63", "#A1887F", "#5D4037", studs=False)
        # 3 tiered voxel leaves (pine style)
        self._draw_3d_cube(root_x - 30, ground_y - trunk_h - 18, 60, 20, 8, 6, "#27AE60", "#2ECC71", "#1E8449", studs=False)
        self._draw_3d_cube(root_x - 22, ground_y - trunk_h - 36, 44, 20, 7, 5, "#229954", "#27AE60", "#196F3D", studs=False)
        self._draw_3d_cube(root_x - 14, ground_y - trunk_h - 52, 28, 18, 6, 4, "#1E8449", "#229954", "#145A32", studs=False)

    def _draw_avatar_mascot(self, width: int, height: int) -> None:
        """
        Draws the friendly Blocky Student/Avatar ("Blocky Bob" / "Coder Alex")
        with real-time animated breathing and an interactive speech bubble.
        """
        ground_y = int(height * 0.62)
        center_x = int(width * 0.12) if self.mode == "BST" else int(width * 0.44)
        bob_offset = int(math.sin(self.bob_phase) * 2.5)
        base_y = ground_y - 8 + bob_offset

        # Avatar pedestal / small voxel stone
        self._draw_3d_cube(center_x - 35, ground_y - 6, 70, 14, 8, 6, "#95A5A6", "#BDC3C7", "#7F8C8D", studs=True)

        # Avatar Legs (Dark Blue Voxel Blocks)
        leg_w = 11
        leg_h = 24
        self._draw_3d_cube(center_x - 14, base_y - leg_h, leg_w, leg_h, 4, 3, "#1A5276", "#2980B9", "#154360", studs=False)
        self._draw_3d_cube(center_x + 3, base_y - leg_h, leg_w, leg_h, 4, 3, "#1A5276", "#2980B9", "#154360", studs=False)

        # Avatar Torso (Electric Cyan/Blue Roblox Hoodie with DSA Badge)
        torso_w = 30
        torso_h = 30
        torso_y = base_y - leg_h - torso_h
        self._draw_3d_cube(center_x - torso_w // 2, torso_y, torso_w, torso_h, 6, 4, "#2980B9", "#3498DB", "#1B4F72", studs=False)
        # DSA Badge on shirt
        self.create_text(center_x + 2, torso_y + 15, text="DSA", font=("Segoe UI", 7, "bold"), fill="#F1C40F")

        # Avatar Arms
        arm_w = 8
        arm_h = 26
        # Left arm
        self._draw_3d_cube(center_x - torso_w // 2 - arm_w - 1, torso_y + 2, arm_w, arm_h, 4, 3, "#F39C12", "#F5B041", "#B9770E", studs=False)
        # Right waving arm
        wave_y = torso_y - 8 + int(math.sin(self.bob_phase * 2) * 4)
        self._draw_3d_cube(center_x + torso_w // 2 + 1, wave_y, arm_w, arm_h, 4, 3, "#F39C12", "#F5B041", "#B9770E", studs=False)

        # Avatar Head (Yellow Roblox Voxel Head)
        head_w = 24
        head_h = 22
        head_y = torso_y - head_h - 2
        self._draw_3d_cube(center_x - head_w // 2, head_y, head_w, head_h, 6, 5, "#F1C40F", "#F9E79F", "#B7950B", studs=False)

        # Head Cap (Cool Red/Black Beanie/Graduation Cap)
        cap_h = 8
        self._draw_3d_cube(center_x - head_w // 2 - 2, head_y - cap_h + 3, head_w + 4, cap_h, 6, 5, "#C0392B", "#E74C3C", "#922B21", studs=False)

        # Friendly Face details
        face_x = center_x
        face_y = head_y + 11
        # Eyes
        self.create_oval(face_x - 6, face_y - 3, face_x - 3, face_y, fill="#17202A", outline="")
        self.create_oval(face_x + 3, face_y - 3, face_x + 6, face_y, fill="#17202A", outline="")
        # Smile
        self.create_arc(face_x - 5, face_y - 1, face_x + 5, face_y + 6, start=190, extent=160, style=tk.ARC, width=2, outline="#17202A")
        # Rosy cheeks
        self.create_oval(face_x - 9, face_y + 1, face_x - 6, face_y + 4, fill="#F1948A", outline="")
        self.create_oval(face_x + 6, face_y + 1, face_x + 9, face_y + 4, fill="#F1948A", outline="")

        # Speech Bubble above Avatar
        self._draw_speech_bubble(center_x, head_y - 14, width)

    def _draw_speech_bubble(self, anchor_x: int, anchor_y: int, max_width: int) -> None:
        text = self.avatar_speech
        bubble_w = min(360, max(220, len(text) * 7))
        bubble_h = 58
        bx = max(10, min(anchor_x - bubble_w // 2, max_width - bubble_w - 20))
        by = max(15, anchor_y - bubble_h - 12)

        # Speech bubble background with soft shadow
        self.create_rectangle(bx + 3, by + 3, bx + bubble_w + 3, by + bubble_h + 3, fill="#2C3E50", outline="")
        self.create_rectangle(bx, by, bx + bubble_w, by + bubble_h, fill="#FFFFFF", outline="#34495E", width=2)

        # Speech pointer triangle
        ptr_tip_x = anchor_x
        ptr_tip_y = anchor_y
        ptr_b1_x = anchor_x - 8
        ptr_b2_x = anchor_x + 8
        self.create_polygon(ptr_b1_x, by + bubble_h, ptr_b2_x, by + bubble_h, ptr_tip_x, ptr_tip_y, fill="#FFFFFF", outline="#34495E", width=2)
        # Cover seam
        self.create_line(ptr_b1_x + 1, by + bubble_h, ptr_b2_x - 1, by + bubble_h, fill="#FFFFFF", width=3)

        # Message Header & Text
        self.create_text(
            bx + 10, by + 12,
            text="🤖 CODER BOB SAYS:",
            font=("Segoe UI", 7, "bold"),
            fill="#E67E22",
            anchor="w"
        )
        self.create_text(
            bx + 10, by + 34,
            text=text,
            font=("Segoe UI", 8, "bold"),
            fill="#2C3E50",
            anchor="w",
            width=bubble_w - 20
        )

    # -------------------------------------------------------------------------
    # 3D ISOMETRIC / VOXEL BLOCK DRAWING ENGINE
    # -------------------------------------------------------------------------
    def _draw_3d_cube(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        off_x: float,
        off_y: float,
        col_front: str,
        col_top: str,
        col_side: str,
        studs: bool = True,
        outline: str = "#2C3E50"
    ) -> None:
        """
        Renders a 3D isometric/oblique rectangular block with 3 visible faces
        and optional toy studs on the top face.
        """
        # 1. Top Face Parallelogram
        top_pts = [
            x, y,
            x + off_x, y - off_y,
            x + width + off_x, y - off_y,
            x + width, y
        ]
        self.create_polygon(top_pts, fill=col_top, outline=outline, width=1)

        # Studs on Top Face (Roblox Toy Block Aesthetic!)
        if studs and width >= 30 and height >= 18:
            stud_count = 3 if width >= 70 else 2
            dx = width / (stud_count + 1)
            for i in range(1, stud_count + 1):
                sx = x + i * dx + off_x * 0.5
                sy = y - off_y * 0.5
                # Stud top disc and skirt
                self.create_oval(sx - 5, sy - 2.5, sx + 5, sy + 2.5, fill=col_top, outline=outline, width=1)
                self.create_arc(sx - 5, sy - 1, sx + 5, sy + 4, start=180, extent=180, style=tk.CHORD, fill=col_side, outline=outline, width=1)

        # 2. Right Side Face Parallelogram
        side_pts = [
            x + width, y,
            x + width + off_x, y - off_y,
            x + width + off_x, y + height - off_y,
            x + width, y + height
        ]
        self.create_polygon(side_pts, fill=col_side, outline=outline, width=1)

        # 3. Front Face Rectangle
        self.create_rectangle(x, y, x + width, y + height, fill=col_front, outline=outline, width=1.5)

    def _draw_labeled_dsa_block(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        value: Any,
        color_idx: int,
        highlight: bool = False,
        tag: str = "block"
    ) -> None:
        """
        Draws a fully branded 3D DSA block with item value and top studs.
        """
        palette = BLOCK_PALETTES[color_idx % len(BLOCK_PALETTES)]
        off_x = 12.0
        off_y = 9.0

        outline_color = "#F39C12" if highlight else "#1A252F"
        outline_width = 3 if highlight else 1.5

        # Glow ring if highlighted (Peek/Inspect)
        if highlight:
            self.create_rectangle(
                x - 6, y - off_y - 6,
                x + width + off_x + 6, y + height + 6,
                outline="#F1C40F", width=3, dash=(4, 2)
            )

        # 3D block
        self._draw_3d_cube(
            x, y, width, height,
            off_x, off_y,
            palette["front"], palette["top"], palette["side"],
            studs=True,
            outline=outline_color
        )

        # Centered bold value label
        val_str = str(value)
        if len(val_str) > 7:
            val_str = val_str[:6] + "…"

        self.create_text(
            x + width / 2,
            y + height / 2,
            text=val_str,
            font=("Segoe UI", 11, "bold"),
            fill=palette["text"],
            tags=tag
        )

    # -------------------------------------------------------------------------
    # STACK VISUALIZATION (Vertical Tower)
    # -------------------------------------------------------------------------
    def _draw_stack_platform(self, width: int, height: int) -> None:
        ground_y = int(height * 0.62)
        base_x = int(width * 0.16)
        block_w = 110
        block_h = 32
        cap = self.stack_ref.capacity if self.stack_ref else 7
        pedestal_y = ground_y - 12

        # 1. Base Pedestal (Obsidian Stone Block)
        self._draw_3d_cube(
            base_x - 18, pedestal_y, block_w + 36, 20,
            14, 10,
            "#34495E", "#4A6572", "#212F3D",
            studs=True
        )

        # Title Tag
        self.create_text(
            base_x + block_w / 2, pedestal_y + 10,
            text="📦 STACK (LIFO)",
            font=("Segoe UI", 9, "bold"),
            fill="#ECF0F1"
        )

        # 2. Vertical Slot Trays / Guide Rails
        for i in range(cap):
            slot_y = pedestal_y - 10 - (i + 1) * (block_h + 4)
            # Dashed ghost placeholder
            self.create_rectangle(
                base_x, slot_y, base_x + block_w, slot_y + block_h,
                outline="#A9CCE3", dash=(2, 3), width=1
            )
            # Level tick
            self.create_text(
                base_x - 12, slot_y + block_h / 2,
                text=f"[{i}]",
                font=("Consolas", 8, "bold"),
                fill="#2C3E50"
            )

        # 3. Render actual stacked blocks
        items = self.stack_ref.to_list() if self.stack_ref else []
        for i, val in enumerate(items):
            slot_y = pedestal_y - 10 - (i + 1) * (block_h + 4)
            is_hl = (self.highlighted_stack_idx == i)
            self._draw_labeled_dsa_block(base_x, slot_y, block_w, block_h, val, i, highlight=is_hl)

        # 4. TOP Pointer (Bouncing Golden Crown Badge)
        if items:
            top_idx = len(items) - 1
            top_y = pedestal_y - 10 - (top_idx + 1) * (block_h + 4)
            badge_x = base_x + block_w + 30
            badge_y = top_y + block_h / 2

            # Pointer arrow
            self.create_polygon(
                badge_x - 10, badge_y,
                badge_x - 2, badge_y - 6,
                badge_x - 2, badge_y + 6,
                fill="#F39C12", outline="#B9770E"
            )
            # Rounded Badge
            self.create_rectangle(
                badge_x, badge_y - 12,
                badge_x + 92, badge_y + 12,
                fill="#F1C40F", outline="#B7950B", width=2
            )
            self.create_text(
                badge_x + 46, badge_y,
                text="👑 TOP [LIFO]",
                font=("Segoe UI", 8, "bold"),
                fill="#7D6608"
            )
        else:
            # Empty Stack Marker
            self.create_text(
                base_x + block_w / 2, pedestal_y - 30,
                text="[ Stack Empty ]",
                font=("Segoe UI", 9, "italic"),
                fill="#566573"
            )

    # -------------------------------------------------------------------------
    # QUEUE VISUALIZATION (Horizontal Conveyor Runway)
    # -------------------------------------------------------------------------
    def _draw_queue_platform(self, width: int, height: int) -> None:
        ground_y = int(height * 0.62)
        conveyor_x = int(width * 0.56)
        block_w = 46
        block_h = 32
        gap = 10
        cap = self.queue_ref.capacity if self.queue_ref else 7
        total_len = cap * (block_w + gap) + 30
        conveyor_y = ground_y - 12

        # 1. 3D Conveyor Track
        self._draw_3d_cube(
            conveyor_x - 15, conveyor_y, total_len, 20,
            14, 10,
            "#2C3E50", "#34495E", "#1A252F",
            studs=False
        )

        # Chevrons indicating movement direction: >> >> >>
        for ch_x in range(conveyor_x + 20, conveyor_x + total_len - 30, 45):
            self.create_text(
                ch_x, conveyor_y + 10,
                text="⏩",
                font=("Segoe UI", 8),
                fill="#F39C12"
            )

        # Header Title
        self.create_text(
            conveyor_x + total_len / 2, conveyor_y + 10,
            text="🚀 QUEUE (FIFO)",
            font=("Segoe UI", 9, "bold"),
            fill="#FFFFFF"
        )

        # 2. Intake & Exit Markers
        # Left Exit (FRONT / Dequeue)
        self.create_text(
            conveyor_x - 4, conveyor_y + 36,
            text="🚀 EXIT\n(Dequeue)",
            font=("Segoe UI", 8, "bold"),
            fill="#1E8449",
            justify="center"
        )
        # Right Intake (REAR / Enqueue)
        self.create_text(
            conveyor_x + total_len - 15, conveyor_y + 36,
            text="📥 INTAKE\n(Enqueue)",
            font=("Segoe UI", 8, "bold"),
            fill="#884EA0",
            justify="center"
        )

        # 3. Slot placeholders
        for i in range(cap):
            slot_x = conveyor_x + 10 + i * (block_w + gap)
            slot_y = conveyor_y - block_h - 10
            self.create_rectangle(
                slot_x, slot_y, slot_x + block_w, slot_y + block_h,
                outline="#AED6F1", dash=(2, 3), width=1
            )
            # Slot index
            self.create_text(
                slot_x + block_w / 2, slot_y + block_h + 8,
                text=f"[{i}]",
                font=("Consolas", 7, "bold"),
                fill="#34495E"
            )

        # 4. Render actual Queue blocks
        items = self.queue_ref.to_list() if self.queue_ref else []
        for i, val in enumerate(items):
            slot_x = conveyor_x + 10 + i * (block_w + gap)
            slot_y = conveyor_y - block_h - 10
            is_hl = (self.highlighted_queue_idx == i)
            self._draw_labeled_dsa_block(slot_x, slot_y, block_w, block_h, val, i + 2, highlight=is_hl)

        # 5. FRONT & REAR Pointer Badges
        if items:
            q_size = len(items)

            # FRONT Pointer (above index 0)
            front_x = conveyor_x + 10 + block_w / 2
            front_y = conveyor_y - block_h - 32
            self.create_rectangle(
                front_x - 32, front_y - 12,
                front_x + 32, front_y + 8,
                fill="#00BCD4", outline="#00838F", width=2
            )
            self.create_text(
                front_x, front_y - 2,
                text="⬅ FRONT",
                font=("Segoe UI", 7, "bold"),
                fill="#FFFFFF"
            )
            self.create_polygon(
                front_x - 4, front_y + 8,
                front_x + 4, front_y + 8,
                front_x, front_y + 14,
                fill="#00BCD4", outline="#00838F"
            )

            # REAR Pointer (above index q_size - 1)
            rear_slot_x = conveyor_x + 10 + (q_size - 1) * (block_w + gap) + block_w / 2
            rear_y = conveyor_y - block_h - 32
            # Offset slightly if q_size == 1 so they don't overlap completely
            if q_size == 1:
                rear_y -= 22

            self.create_rectangle(
                rear_slot_x - 30, rear_y - 12,
                rear_slot_x + 30, rear_y + 8,
                fill="#E91E63", outline="#AD1457", width=2
            )
            self.create_text(
                rear_slot_x, rear_y - 2,
                text="REAR ➡",
                font=("Segoe UI", 7, "bold"),
                fill="#FFFFFF"
            )
            self.create_polygon(
                rear_slot_x - 4, rear_y + 8,
                rear_slot_x + 4, rear_y + 8,
                rear_slot_x, rear_y + 14,
                fill="#E91E63", outline="#AD1457"
            )
        else:
            # Empty Queue Marker
            self.create_text(
                conveyor_x + total_len / 2, conveyor_y - 25,
                text="[ Queue Empty ]",
                font=("Segoe UI", 9, "italic"),
                fill="#566573"
            )

    # -------------------------------------------------------------------------
    # ANIMATIONS (Pure Tkinter Canvas .after(), Zero time.sleep())
    # -------------------------------------------------------------------------
    def animate_stack_push(
        self,
        value: Any,
        target_idx: int,
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """
        Animates a 3D block dropping from the sky into its Stack slot.
        """
        if not animate or not self.winfo_exists():
            self.is_animating = False
            self.redraw()
            on_complete()
            return

        self.is_animating = True
        width = self.winfo_width() or 850
        height = self.winfo_height() or 550
        ground_y = int(height * 0.62)
        base_x = int(width * 0.16)
        block_w = 110
        block_h = 32
        pedestal_y = ground_y - 12
        target_y = pedestal_y - 10 - (target_idx + 1) * (block_h + 4)

        start_y = 20.0
        frames = 10
        cur_frame = 0

        def _step():
            if not self.winfo_exists():
                self.is_animating = False
                return

            nonlocal cur_frame
            cur_frame += 1
            progress = cur_frame / frames
            eased = 1 - pow(1 - progress, 3)
            current_y = start_y + (target_y - start_y) * eased

            self.redraw()
            self._draw_labeled_dsa_block(base_x, current_y, block_w, block_h, value, target_idx)

            if cur_frame < frames:
                self._anim_after_id = self.after(25, _step)
            else:
                self.is_animating = False
                self.redraw()
                on_complete()

        _step()

    def animate_stack_pop(
        self,
        value: Any,
        start_idx: int,
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """
        Animates the top Stack block lifting upward into the sky and fading.
        """
        if not animate or not self.winfo_exists():
            self.is_animating = False
            self.redraw()
            on_complete()
            return

        self.is_animating = True
        width = self.winfo_width() or 850
        height = self.winfo_height() or 550
        ground_y = int(height * 0.62)
        base_x = int(width * 0.16)
        block_w = 110
        block_h = 32
        pedestal_y = ground_y - 12
        start_y = pedestal_y - 10 - (start_idx + 1) * (block_h + 4)

        target_y = start_y - 90
        frames = 9
        cur_frame = 0

        def _step():
            if not self.winfo_exists():
                self.is_animating = False
                return

            nonlocal cur_frame
            cur_frame += 1
            progress = cur_frame / frames
            current_y = start_y + (target_y - start_y) * progress
            current_x = base_x + progress * 40

            self.redraw()
            self._draw_labeled_dsa_block(current_x, current_y, block_w, block_h, value, start_idx)

            if cur_frame < frames:
                self._anim_after_id = self.after(25, _step)
            else:
                self.is_animating = False
                self.redraw()
                on_complete()

        _step()

    def animate_queue_enqueue(
        self,
        value: Any,
        target_idx: int,
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """
        Animates a new block sliding in from the right conveyor ramp to its REAR slot.
        """
        if not animate or not self.winfo_exists():
            self.is_animating = False
            self.redraw()
            on_complete()
            return

        self.is_animating = True
        width = self.winfo_width() or 850
        height = self.winfo_height() or 550
        ground_y = int(height * 0.62)
        conveyor_x = int(width * 0.56)
        block_w = 46
        block_h = 32
        gap = 10
        conveyor_y = ground_y - 12
        target_x = conveyor_x + 10 + target_idx * (block_w + gap)
        slot_y = conveyor_y - block_h - 10

        start_x = width - 40.0
        frames = 11
        cur_frame = 0

        def _step():
            if not self.winfo_exists():
                self.is_animating = False
                return

            nonlocal cur_frame
            cur_frame += 1
            progress = cur_frame / frames
            eased = 1 - pow(1 - progress, 2)
            current_x = start_x + (target_x - start_x) * eased

            self.redraw()
            self._draw_labeled_dsa_block(current_x, slot_y, block_w, block_h, value, target_idx + 2)

            if cur_frame < frames:
                self._anim_after_id = self.after(25, _step)
            else:
                self.is_animating = False
                self.redraw()
                on_complete()

        _step()

    def animate_queue_dequeue(
        self,
        value: Any,
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """
        Animates the FRONT block rolling off the left conveyor exit.
        """
        if not animate or not self.winfo_exists():
            self.is_animating = False
            self.redraw()
            on_complete()
            return

        self.is_animating = True
        width = self.winfo_width() or 850
        height = self.winfo_height() or 550
        ground_y = int(height * 0.62)
        conveyor_x = int(width * 0.56)
        block_w = 46
        block_h = 32
        conveyor_y = ground_y - 12
        start_x = conveyor_x + 10
        slot_y = conveyor_y - block_h - 10

        target_x = conveyor_x - 90.0
        frames = 10
        cur_frame = 0

        def _step():
            if not self.winfo_exists():
                self.is_animating = False
                return

            nonlocal cur_frame
            cur_frame += 1
            progress = cur_frame / frames
            current_x = start_x + (target_x - start_x) * progress
            current_y = slot_y + progress * 20

            self.redraw()
            self._draw_labeled_dsa_block(current_x, current_y, block_w, block_h, value, 2)

            if cur_frame < frames:
                self._anim_after_id = self.after(25, _step)
            else:
                self.is_animating = False
                self.redraw()
                on_complete()

        _step()

    def highlight_stack_element(self, index: int, duration_ms: int = 1200) -> None:
        """Pulse highlights a Stack element (e.g. for Peek)."""
        self.highlighted_stack_idx = index
        self.redraw()

        def _clear():
            self.highlighted_stack_idx = None
            self.redraw()

        self.after(duration_ms, _clear)

    def highlight_queue_element(self, index: int, duration_ms: int = 1200) -> None:
        """Pulse highlights a Queue element (e.g. for Front or Rear peek)."""
        self.highlighted_queue_idx = index
        self.redraw()

        def _clear():
            self.highlighted_queue_idx = None
            self.redraw()

        self.after(duration_ms, _clear)

    # -------------------------------------------------------------------------
    # BINARY SEARCH TREE (BST) VISUALIZATION & 3D PLATFORM
    # -------------------------------------------------------------------------
    def _draw_bst_platform(self, width: int, height: int) -> None:
        """
        Renders the Binary Search Tree in the 3D Roblox blocky world.
        Includes floating 3D grass/stone platforms, 3D connector beams,
        branch indicators ('L'/'R'), 3D isometric node blocks with studs,
        and root crown badge.
        """
        if self.bst_ref is None or self.bst_ref.is_empty():
            # Empty tree banner & stone pedestal
            ped_w = 260
            ped_h = 30
            ped_x = width // 2 - ped_w // 2
            ped_y = int(height * 0.40)

            self._draw_3d_cube(
                ped_x, ped_y, ped_w, ped_h,
                14, 10,
                "#334155", "#475569", "#1E293B",
                studs=True
            )
            self.create_text(
                width // 2, ped_y + 15,
                text="🌳 BST EXPLORER — EMPTY TREE",
                font=("Segoe UI", 9, "bold"),
                fill="#F8FAFC"
            )
            self.create_text(
                width // 2, ped_y + ped_h + 22,
                text="Insert an integer (e.g. 50) or click 'Load Sample Tree' to begin!",
                font=("Segoe UI", 9, "italic"),
                fill="#1E293B"
            )
            return

        # Calculate automatic non-overlapping 3D layout coordinates
        layout = self.bst_ref.calculate_layout(width, height, node_width=52, node_height=34)

        # Floating Roblox header label
        header_w = 300
        hx = width // 2 - header_w // 2
        self.create_rectangle(hx, 10, hx + header_w, 36, fill="#0F172A", outline="#38BDF8", width=1.5)
        self.create_text(
            width // 2, 23,
            text="🌳 3D BINARY SEARCH TREE WORLD",
            font=("Segoe UI", 9, "bold"),
            fill="#FACC15"
        )

        bw = 52.0
        bh = 34.0
        off_x = 10.0
        off_y = 8.0

        # 1. Draw 3D Connecting Beams between parent and child nodes
        edges = self.bst_ref.get_all_edges()
        for parent, child, direction in edges:
            if parent.value not in layout or child.value not in layout:
                continue

            px, py, _ = layout[parent.value]
            cx, cy, _ = layout[child.value]

            p_bottom_x = px + bw / 2 + off_x / 2
            p_bottom_y = py + bh
            c_top_x = cx + bw / 2 + off_x / 2
            c_top_y = cy - off_y / 2

            is_beam_hl = (self.bst_beam_highlight == (parent.value, child.value))

            # 3D Drop Shadow for beam
            self.create_line(
                p_bottom_x, p_bottom_y + 3,
                c_top_x, c_top_y + 3,
                fill="#0F172A", width=6
            )

            if is_beam_hl:
                # Glowing traversal beam
                self.create_line(
                    p_bottom_x, p_bottom_y,
                    c_top_x, c_top_y,
                    fill="#FEF08A", width=8
                )
                self.create_line(
                    p_bottom_x, p_bottom_y,
                    c_top_x, c_top_y,
                    fill="#FACC15", width=5
                )
            else:
                # Cool Cyber Blue (L) or Vibrant Purple (R) Roblox Beams
                beam_color = "#38BDF8" if direction == "L" else "#C084FC"
                self.create_line(
                    p_bottom_x, p_bottom_y,
                    c_top_x, c_top_y,
                    fill=beam_color, width=4
                )

            # Midpoint directional branch badge ("L" or "R")
            mx = (p_bottom_x + c_top_x) / 2
            my = (p_bottom_y + c_top_y) / 2
            badge_color = "#0284C7" if direction == "L" else "#9333EA"
            self.create_oval(
                mx - 8, my - 8, mx + 8, my + 8,
                fill="#0F172A", outline=badge_color, width=1.5
            )
            self.create_text(
                mx, my,
                text=direction,
                font=("Segoe UI", 7, "bold"),
                fill="#FFFFFF"
            )

        # 2. Draw 3D Node Blocks
        for val, (nx, ny, depth) in layout.items():
            is_dup = (self.bst_duplicate_node == val)
            is_hl = (self.highlighted_bst_node == val)
            is_vis = (val in self.bst_visited_nodes)

            if is_dup:
                palette = {"front": "#EF4444", "top": "#F87171", "side": "#B91C1C", "text": "#FFFFFF"}
                self.create_rectangle(
                    nx - 5, ny - off_y - 5,
                    nx + bw + off_x + 5, ny + bh + 5,
                    outline="#DC2626", width=3, dash=(4, 2)
                )
            elif is_hl:
                palette = {"front": "#F59E0B", "top": "#FDE047", "side": "#B45309", "text": "#0F172A"}
                self.create_rectangle(
                    nx - 5, ny - off_y - 5,
                    nx + bw + off_x + 5, ny + bh + 5,
                    outline="#FACC15", width=3, dash=(4, 2)
                )
            elif is_vis:
                palette = {"front": "#10B981", "top": "#6EE7B7", "side": "#047857", "text": "#FFFFFF"}
                self.create_rectangle(
                    nx - 4, ny - off_y - 4,
                    nx + bw + off_x + 4, ny + bh + 4,
                    outline="#34D399", width=2
                )
            else:
                root_val = self.bst_ref.root.value if self.bst_ref.root else 0
                side_branch = 0 if val < root_val else (2 if val > root_val else 1)
                p_idx = (depth * 2 + side_branch) % len(BLOCK_PALETTES)
                palette = BLOCK_PALETTES[p_idx]

            outline_c = "#FACC15" if is_hl else ("#DC2626" if is_dup else "#1E293B")
            self._draw_3d_cube(
                nx, ny, bw, bh,
                off_x, off_y,
                palette["front"], palette["top"], palette["side"],
                studs=True,
                outline=outline_c
            )

            # Center node key label
            self.create_text(
                nx + bw / 2, ny + bh / 2,
                text=str(val),
                font=("Segoe UI", 11, "bold"),
                fill=palette["text"]
            )

            # If Root node, display floating 3D golden crown badge
            if self.bst_ref.root and val == self.bst_ref.root.value:
                crown_w = 66
                crown_x = nx + bw / 2
                crown_y = ny - off_y - 18
                self.create_rectangle(
                    crown_x - crown_w / 2, crown_y - 10,
                    crown_x + crown_w / 2, crown_y + 8,
                    fill="#FACC15", outline="#B45309", width=1.5
                )
                self.create_text(
                    crown_x, crown_y - 1,
                    text="👑 ROOT",
                    font=("Segoe UI", 7, "bold"),
                    fill="#78350F"
                )
                self.create_polygon(
                    crown_x - 4, crown_y + 8,
                    crown_x + 4, crown_y + 8,
                    crown_x, crown_y + 13,
                    fill="#FACC15", outline="#B45309"
                )

    # -------------------------------------------------------------------------
    # BST ANIMATIONS (NON-BLOCKING)
    # -------------------------------------------------------------------------
    def animate_bst_insert(
        self,
        value: int,
        path: List[int],
        steps: List[str],
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """
        Step-by-step path comparison animation, followed by a 3D block
        dropping from the sky into its calculated node position.
        """
        if not animate or not self.winfo_exists():
            self.is_animating = False
            self.clear_bst_highlights()
            on_complete()
            return

        self.is_animating = True
        step_idx = 0

        def _step_path():
            if not self.winfo_exists():
                self.is_animating = False
                return

            nonlocal step_idx
            if step_idx < len(path) - 1:
                cur_node = path[step_idx]
                next_node = path[step_idx + 1]
                self.highlighted_bst_node = cur_node
                self.bst_beam_highlight = (cur_node, next_node)
                if step_idx < len(steps):
                    self.set_speech(steps[step_idx])
                else:
                    self.set_speech(f"Navigating: {cur_node} ➔ {next_node}")
                self.redraw()
                step_idx += 1
                self._anim_after_id = self.after(350, _step_path)
            else:
                # Finished path traversal; now animate the new block dropping in!
                _drop_new_block()

        def _drop_new_block():
            if not self.winfo_exists():
                self.is_animating = False
                return

            # Target position from layout
            width = self.winfo_width() or 850
            height = self.winfo_height() or 550
            layout = self.bst_ref.calculate_layout(width, height) if self.bst_ref else {}

            target_x, target_y, _ = layout.get(value, (width // 2, 80, 0))
            bw, bh = 52.0, 34.0
            start_y = 15.0
            frames = 8
            cur_frame = 0

            def _drop_step():
                if not self.winfo_exists():
                    self.is_animating = False
                    return

                nonlocal cur_frame
                cur_frame += 1
                prog = cur_frame / frames
                eased = 1 - pow(1 - prog, 3)
                cur_y = start_y + (target_y - start_y) * eased

                self.redraw()
                # Draw falling block
                self._draw_labeled_dsa_block(target_x, cur_y, bw, bh, value, 0, highlight=True)

                if cur_frame < frames:
                    self._anim_after_id = self.after(25, _drop_step)
                else:
                    self.is_animating = False
                    self.clear_bst_highlights()
                    self.set_speech(f"Node {value} inserted successfully! BST property maintained.")
                    self.redraw()
                    on_complete()

            _drop_step()

        _step_path()

    def animate_bst_duplicate(
        self,
        value: int,
        path: List[int],
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """Pulsing red alert animation rejecting duplicate value."""
        if not animate or not self.winfo_exists():
            self.clear_bst_highlights()
            on_complete()
            return

        self.is_animating = True
        self.bst_duplicate_node = value
        self.set_speech(f"Duplicate value {value} rejected! BST keys must be unique.")
        self.redraw()

        def _clear_dup():
            self.is_animating = False
            self.bst_duplicate_node = None
            self.redraw()
            on_complete()

        self._anim_after_id = self.after(850, _clear_dup)

    def animate_bst_search(
        self,
        value: int,
        path: List[int],
        found: bool,
        steps: List[str],
        on_complete: Callable[[], None],
        animate: bool = True
    ) -> None:
        """Step-by-step search path highlighting."""
        if not animate or not self.winfo_exists():
            self.clear_bst_highlights()
            on_complete()
            return

        self.is_animating = True
        step_idx = 0

        def _search_step():
            if not self.winfo_exists():
                self.is_animating = False
                return

            nonlocal step_idx
            if step_idx < len(path):
                cur_node = path[step_idx]
                self.highlighted_bst_node = cur_node
                if step_idx < len(path) - 1:
                    self.bst_beam_highlight = (cur_node, path[step_idx + 1])
                else:
                    self.bst_beam_highlight = None

                if step_idx < len(steps):
                    self.set_speech(steps[step_idx])
                self.redraw()
                step_idx += 1
                self._anim_after_id = self.after(400, _search_step)
            else:
                self.is_animating = False
                if found:
                    self.set_speech(f"Match found! Node {value} exists in the BST.")
                else:
                    self.set_speech(f"Value {value} not found in the BST.")
                self.clear_bst_highlights()
                on_complete()

        _search_step()

    def highlight_bst_node(self, value: int, visited_list: Optional[List[int]] = None) -> None:
        """Highlights a single BST node and visited path (e.g. for traversals)."""
        self.highlighted_bst_node = value
        self.bst_visited_nodes = list(visited_list) if visited_list else []
        self.redraw()

    def clear_bst_highlights(self) -> None:
        """Resets all BST highlight markers."""
        self.highlighted_bst_node = None
        self.bst_beam_highlight = None
        self.bst_visited_nodes = []
        self.bst_duplicate_node = None
        self.redraw()
