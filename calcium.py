import tkinter as tk
from tkinter import ttk
import asyncio
import psutil
#mrcobalt
#cobalt
#altunaltechnologies
class SortCubesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SortCubes - CALCium Engine7")
        self.root.configure(bg="#1e1e1e")
        
        self.speed_map = {
            "Slowest": 1.5, "Slow": 0.7, "Standard": 0.17,
            "Fast": 0.1, "Turbo": 0.05, "Thunderbolt": 0.001, "Instant": 0.00001
        }
        
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        control_frame = tk.Frame(self.root, bg="#1e1e1e")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="input data in integer:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)
        self.user_input = tk.Entry(control_frame, width=20)
        self.user_input.grid(row=0, column=1, padx=5)
        self.user_input.insert(0, "10, 40, 25, 60, 15, 80, 45")

        tk.Label(control_frame, text="engine:", fg="white", bg="#1e1e1e").grid(row=0, column=2, padx=5)
        # Yeni motorlar eklendi: Tim, Cocktail ve Comb
        self.algo_combo = ttk.Combobox(control_frame, values=[
            "Bubble Engine", "Gnome Engine", "Insertion Engine", 
            "Selection Engine", "Merge Engine", "Tim Engine", 
            "Cocktail Engine", "Comb Engine"
        ], state="readonly", width=15)
        self.algo_combo.current(0)
        self.algo_combo.grid(row=0, column=3, padx=5)

        tk.Label(control_frame, text="speedometer:", fg="white", bg="#1e1e1e").grid(row=0, column=4, padx=5)
        self.speed_combo = ttk.Combobox(control_frame, values=list(self.speed_map.keys()) + ["Auto"], state="readonly", width=12)
        self.speed_combo.current(2)
        self.speed_combo.grid(row=0, column=5, padx=5)

        self.start_button = tk.Button(control_frame, text="Execute Engine", command=lambda: asyncio.create_task(self.start_sorting()), bg="#4CAF50", fg="white")
        self.start_button.grid(row=0, column=6, padx=10)

        self.status_label = tk.Label(self.root, text="ready", fg="gray", bg="#1e1e1e")
        self.status_label.pack()

    def get_delay(self):
        mode = self.speed_combo.get()
        if mode == "Auto":
            load = (psutil.cpu_percent() + psutil.virtual_memory().percent) / 2
            if load < 20: return 0.05
            elif load < 50: return 0.2
            else: return 0.8
        return self.speed_map.get(mode, 0.17)

    def draw_towers(self, data, colors):
        self.canvas.delete("all")
        n = len(data)
        if n == 0: return
        width = 800 / (n + 1)
        for i, height in enumerate(data):
            x0 = i * width + 10
            y0 = 400 - (height * 4)
            x1 = (i + 1) * width
            y1 = 400
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="white")
            self.canvas.create_text(x0 + width/2, y0 - 15, text=str(height), fill="white")

    # --- EXISTING ENGINES (Bubble, Gnome, Insertion, Selection, Merge) ---
    async def bubble_sort(self, data):
        n = len(data)
        colors = ["white"] * n
        for i in range(n):
            for j in range(0, n - i - 1):
                colors[j] = colors[j+1] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    self.draw_towers(data, colors)
                colors[j] = colors[j+1] = "white"
            colors[n-i-1] = "green"
        self.draw_towers(data, ["green"]*n)

    async def gnome_sort(self, data):
        n = len(data)
        index = 0
        colors = ["white"] * n
        while index < n:
            if index == 0: index += 1
            colors[index] = colors[index-1] = "red"
            self.draw_towers(data, colors)
            await asyncio.sleep(self.get_delay())
            if data[index] >= data[index - 1]:
                colors[index] = colors[index-1] = "white"
                index += 1
            else:
                data[index], data[index - 1] = data[index - 1], data[index]
                self.draw_towers(data, colors)
                colors[index] = colors[index-1] = "white"
                index -= 1
        self.draw_towers(data, ["green"] * n)

    async def insertion_sort(self, data):
        n = len(data)
        colors = ["white"] * n
        for i in range(1, n):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                colors[j+1] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                data[j+1] = data[j] # mr.cobalt
                colors[j+1] = "white"
                j -= 1
            data[j+1] = key
            colors[i] = "green"
        self.draw_towers(data, ["green"] * n)

    async def selection_sort(self, data):
        n = len(data)
        colors = ["white"] * n
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                colors[j] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                if data[min_idx] > data[j]:
                    min_idx = j
                colors[j] = "white"
            data[i], data[min_idx] = data[min_idx], data[i]
            colors[i] = "green"
        self.draw_towers(data, ["green"] * n)

    async def merge_sort(self, data, start, end):
        if end - start > 1:
            mid = (start + end) // 2
            await self.merge_sort(data, start, mid)
            await self.merge_sort(data, mid, end)
            left = data[start:mid]
            right = data[mid:end]
            i = j = 0
            for k in range(start, end):
                colors = ["white"] * len(data)
                colors[k] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                if i < len(left) and (j >= len(right) or left[i] <= right[j]):
                    data[k] = left[i]
                    i += 1
                else:
                    data[k] = right[j]
                    j += 1
            if start == 0 and end == len(data):
                self.draw_towers(data, ["green"]*len(data))

    # --- NEW ENGINES (Cocktail, Comb, Tim) ---

    async def cocktail_shaker_sort(self, data):
        n = len(data)
        swapped = True
        start = 0
        end = n - 1
        colors = ["white"] * n
        while swapped:
            swapped = False
            for i in range(start, end):
                colors[i] = colors[i+1] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                if data[i] > data[i+1]:
                    data[i], data[i+1] = data[i+1], data[i]
                    swapped = True
                colors[i] = colors[i+1] = "white"
            if not swapped: break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                colors[i] = colors[i+1] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                if data[i] > data[i+1]:
                    data[i], data[i+1] = data[i+1], data[i]
                    swapped = True
                colors[i] = colors[i+1] = "white"
            start += 1
        self.draw_towers(data, ["green"] * n)

    async def comb_sort(self, data):
        n = len(data)
        gap = n
        shrink = 1.3
        sorted = False
        colors = ["white"] * n
        while not sorted:
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted = True
            for i in range(0, n - gap):
                colors[i] = colors[i+gap] = "red"
                self.draw_towers(data, colors)
                await asyncio.sleep(self.get_delay())
                if data[i] > data[i+gap]:
                    data[i], data[i+gap] = data[i+gap], data[i]
                    sorted = False
                colors[i] = colors[i+gap] = "white"
        self.draw_towers(data, ["green"] * n)

    async def tim_sort(self, data):
        # TimSort asenkron hibrit yapı (Insertion + Merge)
        n = len(data)
        RUN = 32
        for i in range(0, n, RUN):
            
            for j in range(i + 1, min(i + RUN, n)):
                key = data[j]
                k = j - 1
                while k >= i and data[k] > key:
                    data[k+1] = data[k]
                    k -= 1
                    self.draw_towers(data, ["red" if x==k or x==k+1 else "white" for x in range(n)])
                    await asyncio.sleep(self.get_delay())
                data[k+1] = key
        
        size = RUN
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(n - 1, left + size - 1)
                right = min((left + 2 * size - 1), (n - 1))
                if mid < right:
                    # Merge 
                    l, r = data[left:mid+1], data[mid+1:right+1]
                    i = j = 0
                    for k in range(left, right + 1):
                        self.draw_towers(data, ["red" if x==k else "white" for x in range(n)])
                        await asyncio.sleep(self.get_delay())
                        if i < len(l) and (j >= len(r) or l[i] <= r[j]):
                            data[k] = l[i]; i += 1
                        else:
                            data[k] = r[j]; j += 1
            size *= 2
        self.draw_towers(data, ["green"] * n)

    async def start_sorting(self):
        try:
            data = [int(x.strip()) for x in self.user_input.get().split(",")]
            algo = self.algo_combo.get()
            self.status_label.config(text=f"Executing {algo}...", fg="yellow")
            
            if algo == "Bubble Engine": await self.bubble_sort(data)
            elif algo == "Gnome Engine": await self.gnome_sort(data)
            elif algo == "Insertion Engine": await self.insertion_sort(data)
            elif algo == "Selection Engine": await self.selection_sort(data)
            elif algo == "Merge Engine": await self.merge_sort(data, 0, len(data))
            elif algo == "Cocktail Engine": await self.cocktail_shaker_sort(data)
            elif algo == "Comb Engine": await self.comb_sort(data)
            elif algo == "Tim Engine": await self.tim_sort(data)
            
            self.status_label.config(text=f"{algo} Sorted Successfully!", fg="green")
        except:
            self.status_label.config(text="E1", fg="red")

async def main():
    root = tk.Tk()
    app = SortCubesGUI(root)
    
    while True:
        try:
            root.update()
            await asyncio.sleep(0.01)
        except tk.TclError:
            break

if __name__ == "__main__":
    asyncio.run(main())