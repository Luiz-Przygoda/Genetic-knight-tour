"""
knight_tour_gui_presentation_final.py
Versão definitiva para apresentação, com tema moderno, gráfico de evolução do GA
e visualização interativa da heurística de Warnsdorff.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import time
from copy import deepcopy
from tkinter import messagebox

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import sv_ttk
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ----------------------------
# Configurações Globais
# ----------------------------
BOARD_SIZE = 8
GA_POP = 250
GA_GEN_LIMIT = 2000
GA_TOURN = 3
GA_MUT_RATE = 0.15
ANIMATION_DELAY = 100

# ----------------------------
# Funções de Lógica do Passeio (sem alterações)
# ----------------------------
KNIGHT_MOVES = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
def inbound(x,y,n): return 0 <= x < n and 0 <= y < n
def idx_to_xy(i,n): return (i % n, i // n)
def xy_to_idx(x,y,n): return y * n + x
def legal_knight_move(a,b,n):
    ax,ay = idx_to_xy(a,n); bx,by = idx_to_xy(b,n)
    return (abs(ax-bx), abs(ay-by)) in [(1,2),(2,1)]
def random_knight_walk(n, start_idx=0):
    """Gera um passeio aleatório de cavalo sem repetir casas (pode não cobrir o tabuleiro todo)."""
    seen = set([start_idx])
    path = [start_idx]
    x, y = idx_to_xy(start_idx, n)
    while True:
        moves = []
        for dx, dy in KNIGHT_MOVES:
            nx, ny = x + dx, y + dy
            if inbound(nx, ny, n):
                idx = xy_to_idx(nx, ny, n)
                if idx not in seen:
                    moves.append(idx)
        if not moves:
            break
        nxt = random.choice(moves)
        path.append(nxt)
        seen.add(nxt)
        x, y = idx_to_xy(nxt, n)
    return path  # pode ter < n*n
def randomized_warnsdorff_extend(n, path):
    """Tenta estender 'path' (lista de índices) sem repetir casas,
    usando Warnsdorff com desempate aleatório."""
    visited = set(path)
    cur = path[-1]
    while True:
        x, y = idx_to_xy(cur, n)
        candidates = []
        for dx, dy in KNIGHT_MOVES:
            nx, ny = x + dx, y + dy
            if inbound(nx, ny, n):
                idx = xy_to_idx(nx, ny, n)
                if idx not in visited:
                    # grau de liberdade do próximo passo
                    deg = 0
                    for dx2, dy2 in KNIGHT_MOVES:
                        nnx, nny = nx + dx2, ny + dy2
                        if inbound(nnx, nny, n):
                            j = xy_to_idx(nnx, nny, n)
                            if j not in visited:
                                deg += 1
                    candidates.append((deg, idx))
        if not candidates:
            break
        # Warnsdorff: escolhe menor grau, porém aleatoriza entre empates
        min_deg = min(d for d, _ in candidates)
        pool = [idx for d, idx in candidates if d == min_deg]
        nxt = random.choice(pool)
        path.append(nxt)
        visited.add(nxt)
        cur = nxt
    return path

def warnsdorff_tour(n, start_idx=0):
    x0,y0 = idx_to_xy(start_idx,n); board = [[-1]*n for _ in range(n)]; path = []
    def degree(x,y):
        d=0
        for dx,dy in KNIGHT_MOVES:
            nx,ny = x+dx, y+dy
            if inbound(nx,ny,n) and board[ny][nx] == -1: d += 1
        return d
    x,y = x0,y0; board[y][x] = 0; path.append(xy_to_idx(x,y,n))
    for step in range(1,n*n):
        moves = []
        for dx,dy in KNIGHT_MOVES:
            nx,ny = x+dx, y+dy
            if inbound(nx,ny,n) and board[ny][nx] == -1: moves.append((degree(nx,ny),(nx,ny)))
        if not moves: return path
        moves.sort(key=lambda t: t[0])
        x,y = moves[0][1]; board[y][x] = step; path.append(xy_to_idx(x,y,n))
    return path

# ... (O resto das funções de lógica backtracking e a classe GeneticKnightTour permanecem as mesmas)
def backtracking_tour(n, start_idx=0, time_limit=5.0):
    start_time = time.time(); sx,sy = idx_to_xy(start_idx,n); visited = [False]*(n*n); path = []
    def dfs(x,y,step):
        if time.time() - start_time > time_limit: return None
        visited[xy_to_idx(x,y,n)] = True; path.append(xy_to_idx(x,y,n))
        if step == n*n: return list(path)
        nexts = []
        for dx,dy in KNIGHT_MOVES:
            nx,ny = x+dx,y+dy
            if inbound(nx,ny,n) and not visited[xy_to_idx(nx,ny,n)]:
                d=0
                for dx2,dy2 in KNIGHT_MOVES:
                    nnx,nny = nx+dx2, ny+dy2
                    if inbound(nnx,nny,n) and not visited[xy_to_idx(nnx,nny,n)]: d+=1
                nexts.append((d,nx,ny))
        nexts.sort(key=lambda t:t[0])
        for _,nx,ny in nexts:
            res = dfs(nx,ny,step+1)
            if res: return res
        visited[xy_to_idx(x,y,n)] = False; path.pop()
        return None
    return dfs(sx,sy,1)

class GeneticKnightTour:
    def __init__(self, n, population_size, mutation_rate, tourn_size):
        self.n = n
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.tourn = tourn_size
        self.population = []
        self.fitnesses = []
        self.generation = 0
        self.best = None               # melhor cromossomo (perm)
        self.best_fitness = -1         # tamanho do prefixo legal - 1 (número de arestas legais)
        self.best_path = None          # caminho 100% legal correspondente a 'best'
        self.best_fitness_history = []
        self.avg_fitness_history = []

    # ---------- Construção e reparo ----------
    def init_population(self, start_idx=0):
        self.generation = 0
        self.best_fitness = -1
        self.best_path = None
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.population = []

        # Em vez de permutações puras, inicialize com passeios de cavalo aleatórios e complete com casas faltantes
        all_cells = set(range(self.n * self.n))
        for _ in range(self.pop_size):
            walk = random_knight_walk(self.n, start_idx=start_idx)
            remaining = list(all_cells - set(walk))
            random.shuffle(remaining)
            chrom = walk + remaining
            self.repair(chrom)  # já sai "legalizado"
            self.population.append(chrom)

        self.evaluate_all()

    def _legal_prefix(self, chrom):
        """Retorna o maior prefixo SEM repetir casas e só com movimentos válidos de cavalo.
           Também retorna a versão 'ajustada' do cromossomo (com swaps locais)."""
        n2 = self.n * self.n
        visited = set([chrom[0]])
        path = [chrom[0]]
        chrom_adj = chrom[:]  # trabalhamos numa cópia

        for i in range(1, n2):
            prev = path[-1]
            cur = chrom_adj[i]

            # se já foi visitado ou o movimento não é legal, tentar achar gene mais à frente alcançável
            if (cur in visited) or (not legal_knight_move(prev, cur, self.n)):
                found = False
                for j in range(i + 1, n2):
                    cand = chrom_adj[j]
                    if cand not in visited and legal_knight_move(prev, cand, self.n):
                        # colocar candidato na posição i
                        chrom_adj[i], chrom_adj[j] = chrom_adj[j], chrom_adj[i]
                        cur = chrom_adj[i]
                        found = True
                        break
                if not found:
                    # não dá para seguir legalmente
                    break

            # agora cur é novo e alcançável
            visited.add(cur)
            path.append(cur)

        return path, chrom_adj

    def repair(self, chrom):
        """Repara um cromossomo para maximizar o prefixo legal via swaps locais.
           O cromossomo original é modificado in-place."""
        path, fixed = self._legal_prefix(chrom)
        chrom[:] = fixed  # sobrescreve com a versão reparada
        return path

    # ---------- Avaliação ----------
    def fitness(self, chrom):
        # 1) obtém prefixo legal (e o cromossomo ajustado)
        base_path, _ = self._legal_prefix(chrom)
        # 2) estende localmente com Warnsdorff aleatório (memético leve)
        extended = randomized_warnsdorff_extend(self.n, base_path[:])
        # fitness = arestas legais do caminho estendido
        return max(0, len(extended) - 1), extended
 
    def evaluate_all(self):
        fits = []
        paths = []
        for ch in self.population:
            f, p = self.fitness(ch)
            fits.append(f)
            paths.append(p)

        self.fitnesses = fits
        current_gen_best = max(range(self.pop_size), key=lambda i: self.fitnesses[i])
        current_best_fit = self.fitnesses[current_gen_best]

        if current_best_fit > self.best_fitness:
            self.best_fitness = current_best_fit
            self.best = self.population[current_gen_best][:]
            self.best_path = paths[current_gen_best][:]

        self.best_fitness_history.append(self.best_fitness)
        self.avg_fitness_history.append(sum(self.fitnesses) / self.pop_size)

    # ---------- Seleção, Crossover, Mutação ----------
    def tournament_select(self):
        k = self.tourn
        candidates = random.sample(range(self.pop_size), k)
        best_idx = max(candidates, key=lambda i: self.fitnesses[i])
        return deepcopy(self.population[best_idx])

    def order_crossover(self, p1, p2):
        n = len(p1)
        a, b = sorted(random.sample(range(n), 2))
        child = [-1] * n
        child[a:b+1] = p1[a:b+1]
        fill_pos = (b + 1) % n
        for gene in p2[b+1:] + p2[:b+1]:
            if gene not in child:
                child[fill_pos] = gene
                fill_pos = (fill_pos + 1) % n
        return child

    def mutate(self, chrom):
        if random.random() < 0.5:
            i, j = random.sample(range(1, len(chrom)), 2)
            chrom[i], chrom[j] = chrom[j], chrom[i]
        else:
            a, b = sorted(random.sample(range(1, len(chrom)), 2))
            chrom[a:b+1] = reversed(chrom[a:b+1])

    # ---------- Loop ----------
    def step(self):
        newpop = [deepcopy(self.best)]  # elitismo (já está reparado)
        while len(newpop) < self.pop_size:
            p1 = self.tournament_select()
            p2 = self.tournament_select()
            child = self.edge_recombination_crossover(p1, p2)
            if random.random() < self.mutation_rate:
                self.mutate(child)
            # Repara o filho antes de entrar na população
            self.repair(child)
            newpop.append(child)

        self.population = newpop
        self.evaluate_all()
        self.generation += 1

    
        return self.best_fitness == (self.n * self.n) - 1
    
    def edge_recombination_crossover(self, p1, p2):
        """ERX: constrói um filho preservando adjacências dos pais."""
        n = len(p1)
        # tabela de adjacências
        adj = {g: set() for g in p1}
        def add_edges(a, b):
            for i in range(n):
                left = a[(i - 1) % n]
                right = a[(i + 1) % n]
                adj[a[i]].update([left, right])
            for i in range(n):
                left = b[(i - 1) % n]
                right = b[(i + 1) % n]
                adj[b[i]].update([left, right])

        add_edges(p1, p2)

        child = []
        used = set()
        cur = p1[0]  # pode variar; simples: começa no primeiro de p1
        for _ in range(n):
            child.append(cur)
            used.add(cur)
            # remove 'cur' das listas adjacentes
            for k in adj:
                adj[k].discard(cur)
            # escolhe próximo:
            # 1) entre adjacentes de cur, pegue aquele cujo set adjacente é menor (mais restrito)
            candidates = [x for x in adj[cur] if x not in used]
            if candidates:
                cur = min(candidates, key=lambda x: len(adj[x]))
            else:
                # 2) se não há adjacente disponível, escolha qualquer gene ainda não usado
                remaining = [g for g in adj.keys() if g not in used]
                if not remaining:
                    break
                cur = random.choice(remaining)
        return child

# ----------------------------
# Classe Principal da GUI
# ----------------------------
class KnightTourGUI:
    def save_ga_graph(self):
        # Abre um diálogo para salvar a figura do GA como PNG/SVG/PDF.
        if not MATPLOTLIB_AVAILABLE or not hasattr(self, "fig"):
            messagebox.showerror("Erro", "Gráfico indisponível (matplotlib não carregado).")
            return

        # Sugestão de nome de arquivo com a geração atual
        gen = getattr(self.ga, "generation", 0) if self.ga else 0
        suggested = f"ga_convergencia_gen{gen}"

        filepath = filedialog.asksaveasfilename(
            title="Salvar gráfico",
            defaultextension=".png",
            initialfile=suggested,
            filetypes=[
                ("PNG", "*.png"),
                ("SVG", "*.svg"),
                ("PDF", "*.pdf"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if not filepath:
            return  # usuário cancelou

        try:
            # Garante que tudo está desenhado antes de salvar
            if hasattr(self, "graph_canvas"):
                self.graph_canvas.draw()

            # Salva com uma resolução boa e sem cortes
            self.fig.savefig(filepath, dpi=150, bbox_inches="tight")
            messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar o gráfico.\n\nDetalhes: {e}")

    def __init__(self, root, n=BOARD_SIZE):
        self.root = root; self.n = n; self.cell_size = 60; self.start_idx = 0; self.path = []
        self.ga = None; self.ga_state = 'idle'; self.animation_state = 'idle'
        self.animation_step = 0; self.current_animation_path = None
        self.start_time = 0; self.elapsed_time_paused = 0; self.last_hover_idx = -1
        self._setup_layout(); self._create_widgets(); self._bind_events(); self.redraw_canvas()

    def _setup_layout(self):
        self.root.grid_rowconfigure(0, weight=1); self.root.grid_columnconfigure(0, weight=3); self.root.grid_columnconfigure(1, weight=1)
        self.canvas_frame = tk.Frame(self.root); self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', highlightthickness=0); self.canvas.pack(fill="both", expand=True)
        self.controls_frame = ttk.Frame(self.root, padding=15); self.controls_frame.grid(row=0, column=1, sticky='nsew')
        self.controls_frame.grid_rowconfigure(3, weight=1) # Faz o frame do gráfico expandir

    def _create_widgets(self):
        # --- Frames de Controles ---
        det_frame = ttk.LabelFrame(self.controls_frame, text="Algoritmos Determinísticos", padding=10); det_frame.pack(fill='x', expand=False, pady=5)
        self.warnsdorff_btn = ttk.Button(det_frame, text="Warnsdorff (Rápido)", command=self.run_warnsdorff); self.warnsdorff_btn.pack(fill='x', pady=2)
        self.backtracking_btn = ttk.Button(det_frame, text="Backtracking (Lento)", command=self.run_backtracking); self.backtracking_btn.pack(fill='x', pady=2)

        ga_frame = ttk.LabelFrame(self.controls_frame, text="Algoritmo Genético", padding=10); ga_frame.pack(fill='x', expand=False, pady=5)
        ttk.Label(ga_frame, text="População:").pack(anchor='w'); self.pop_spin = tk.Spinbox(ga_frame, from_=50, to=2000, increment=50, width=10); self.pop_spin.delete(0,"end"); self.pop_spin.insert(0,str(GA_POP)); self.pop_spin.pack(fill='x', pady=2)
        ttk.Label(ga_frame, text="Taxa de Mutação:").pack(anchor='w'); self.mut_spin = tk.Spinbox(ga_frame, from_=0.0, to=1.0, increment=0.01, width=10, format="%.2f"); self.mut_spin.delete(0,"end"); self.mut_spin.insert(0,str(GA_MUT_RATE)); self.mut_spin.pack(fill='x', pady=2)

        run_frame = ttk.LabelFrame(self.controls_frame, text="Controle de Execução", padding=10); run_frame.pack(fill='x', expand=False, pady=5)
        self.run_ga_btn = ttk.Button(run_frame, text="Iniciar GA", command=self.toggle_ga_run); self.run_ga_btn.pack(fill='x', pady=2)
        self.pause_anim_btn = ttk.Button(run_frame, text="Pausar Animação", command=self.toggle_animation_pause, state=tk.DISABLED); self.pause_anim_btn.pack(fill='x', pady=2)
        self.reset_btn = ttk.Button(run_frame, text="Resetar Tabuleiro", command=self.reset); self.reset_btn.pack(fill='x', pady=2)

        # --- Gráfico do GA ---
        if MATPLOTLIB_AVAILABLE:
            graph_frame = ttk.LabelFrame(self.controls_frame, text="Evolução do GA", padding=10); graph_frame.pack(fill='both', expand=True, pady=10)
            self.fig = plt.Figure(figsize=(4, 3), dpi=100); self.ax_graph = self.fig.add_subplot(111)
            self.graph_canvas = FigureCanvasTkAgg(self.fig, master=graph_frame); self.graph_canvas.get_tk_widget().pack(fill='both', expand=True)
            # Botão para salvar o gráfico como imagem
            self.save_graph_btn = ttk.Button(
                graph_frame,
                text="Salvar gráfico (PNG/SVG/PDF)",
                command=self.save_ga_graph
            )
            self.save_graph_btn.pack(fill='x', pady=(8, 0))
            self.init_ga_graph()
        else: ttk.Label(self.controls_frame, text="Matplotlib não encontrado.\nGráfico indisponível.", foreground="red").pack(pady=10)

        # --- Barra de Status ---
        self.status_bar = ttk.Frame(self.root, padding=5); self.status_bar.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.gen_label = ttk.Label(self.status_bar, text="Geração: -"); self.gen_label.pack(side='left', padx=10)
        self.fit_label = ttk.Label(self.status_bar, text="Aptidão: -"); self.fit_label.pack(side='left', padx=10)
        self.time_label = ttk.Label(self.status_bar, text="Tempo: 0.0s"); self.time_label.pack(side='left', padx=10)
        self.status_label = ttk.Label(self.status_bar, text="Status: Pronto."); self.status_label.pack(side='right', padx=10)

    def _bind_events(self):
        self.canvas_frame.bind("<Configure>", self._on_resize); self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_mouse_hover); self.canvas.bind("<Leave>", lambda e: self.canvas.delete("warnsdorff_viz"))
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def _on_resize(self, event): self.cell_size = max(20, min(event.width, event.height) // self.n); self.redraw_canvas()

    def _on_click(self, event):
        if self.ga_state != 'idle' or self.animation_state != 'idle': return
        c = int(event.x // self.cell_size); r = int(event.y // self.cell_size)
        if inbound(c, r, self.n): self.start_idx = xy_to_idx(c, r, self.n); self.reset(); self.status_label.config(text=f"Ponto inicial: {self.start_idx} ({c},{r})")

    def _on_mouse_hover(self, event):
        if self.ga_state != 'idle' or self.animation_state != 'idle': return
        c, r = int(event.x // self.cell_size), int(event.y // self.cell_size)
        idx = xy_to_idx(c, r, self.n)
        if idx == self.last_hover_idx: return
        self.last_hover_idx = idx
        self.canvas.delete("warnsdorff_viz")
        
        def get_degree(from_idx):
            d = 0; x, y = idx_to_xy(from_idx, self.n)
            for dx, dy in KNIGHT_MOVES:
                if inbound(x+dx, y+dy, self.n): d += 1
            return d
            
        x,y = idx_to_xy(idx, self.n)
        for dx, dy in KNIGHT_MOVES:
            nx, ny = x+dx, y+dy
            if inbound(nx, ny, self.n):
                next_idx = xy_to_idx(nx,ny,self.n)
                degree = get_degree(next_idx)
                cx, cy = nx*self.cell_size+self.cell_size/2, ny*self.cell_size+self.cell_size/2
                self.canvas.create_text(cx, cy, text=str(degree), fill="white", font=('Arial', int(self.cell_size/4), 'bold'), tags="warnsdorff_viz")

    def redraw_canvas(self):
        self.canvas.delete("all")
        for r in range(self.n):
            for c in range(self.n):
                x0,y0 = c*self.cell_size, r*self.cell_size; color = "#f0d9b5" if (r+c)%2==0 else "#b58863"
                self.canvas.create_rectangle(x0,y0,x0+self.cell_size,y0+self.cell_size, fill=color, outline='black')
        if self.path: self._draw_path_snapshot(self.path, len(self.path)-1, is_final=True, is_solution=len(self.path)==self.n*self.n)
        if self.ga_state == 'idle' and self.animation_state == 'idle':
             x,y=idx_to_xy(self.start_idx, self.n); cx,cy=x*self.cell_size+self.cell_size/2, y*self.cell_size+self.cell_size/2
             self.canvas.create_text(cx,cy, text="S", font=('Arial', int(self.cell_size/3), 'bold'), fill='green')

    def _draw_path_snapshot(self, path, current_step, is_final=False, is_solution=False):
        self.canvas.delete("path");
        if not path: return
        def interpolate_color(start, end, frac): r1,g1,b1=self.root.winfo_rgb(start); r2,g2,b2=self.root.winfo_rgb(end); r,g,b = r1+(r2-r1)*frac, g1+(g2-g1)*frac, b1+(b2-b1)*frac; return f'#{int(r)//256:02x}{int(g)//256:02x}{int(b)//256:02x}'
        for i in range(min(current_step, len(path)-1)):
            x1,y1=idx_to_xy(path[i],self.n); x2,y2=idx_to_xy(path[i+1],self.n); cx1,cy1=x1*self.cell_size+self.cell_size/2, y1*self.cell_size+self.cell_size/2; cx2,cy2=x2*self.cell_size+self.cell_size/2, y2*self.cell_size+self.cell_size/2
            color = "gold" if is_solution else interpolate_color("#FFFF00", "#FF4500", i / max(1, len(path)-1)); self.canvas.create_line(cx1,cy1,cx2,cy2, width=3, fill=color, tags="path")
        for i, idx in enumerate(path[:current_step+1]):
            x,y=idx_to_xy(idx, self.n); cx,cy=x*self.cell_size+self.cell_size/2, y*self.cell_size+self.cell_size/2
            if i == current_step and not is_final: self.canvas.create_text(cx,cy, text="♞", font=('Arial', int(self.cell_size/1.5)), fill='black', tags="path")
            else: r=self.cell_size/4; self.canvas.create_oval(cx-r,cy-r,cx+r,cy+r, fill='lightblue', outline='darkblue', tags="path"); self.canvas.create_text(cx,cy, text=str(i+1), font=('Arial',int(self.cell_size/5),'bold'), tags="path")

    def animate_path(self, path, is_solution=False):
        if not path or self.animation_state != 'idle': return
        self.current_animation_path=path; self.animation_step=0; self.animation_state='running'
        self._toggle_controls(tk.DISABLED); self.pause_anim_btn.config(state=tk.NORMAL, text="Pausar Animação")
        self.animation_loop(is_solution)

    def animation_loop(self, is_solution):
        if self.animation_state != 'running': return
        if self.animation_step >= len(self.current_animation_path):
            self.animation_state='idle'; self._toggle_controls(tk.NORMAL); self.pause_anim_btn.config(state=tk.DISABLED)
            if is_solution: self.flash_solution(); self._update_status(message="SOLUÇÃO ENCONTRADA!", color="green")
            else: self._update_status(message="Animação concluída.")
            return
        self._draw_path_snapshot(self.current_animation_path, self.animation_step, is_solution=is_solution)
        self._update_status(message=f"Animação: Passo {self.animation_step+1}/{len(self.current_animation_path)}")
        self.animation_step += 1
        self.root.after(ANIMATION_DELAY, self.animation_loop, is_solution)

    def toggle_animation_pause(self):
        if self.animation_state == 'running': self.animation_state='paused'; self.pause_anim_btn.config(text="Continuar Animação"); self._update_status(message=f"Animação pausada no passo {self.animation_step}.")
        elif self.animation_state == 'paused': self.animation_state='running'; self.pause_anim_btn.config(text="Pausar Animação"); self.animation_loop(len(self.current_animation_path)==self.n*self.n)

    def flash_solution(self):
        def flash(count):
            if count <= 0 or self.animation_state != 'idle': self.redraw_canvas(); return
            color = "gold" if count % 2 != 0 else "#f0d9b5"
            self.canvas.itemconfig("path", fill=color); self.root.after(300, flash, count-1)
        flash(5)

    def _toggle_controls(self, state):
        for w in [self.warnsdorff_btn, self.backtracking_btn, self.reset_btn, self.pop_spin, self.mut_spin]: w.config(state=state)
        self.run_ga_btn.config(state=tk.DISABLED if state==tk.DISABLED else tk.NORMAL)
        if self.animation_state != 'idle': self.run_ga_btn.config(state=tk.DISABLED)

    def _update_status(self, gen=None, fitness=None, total=None, elapsed=None, message=None, color=None):
        if gen is not None: self.gen_label.config(text=f"Geração: {gen}")
        if fitness is not None: self.fit_label.config(text=f"Aptidão: {fitness}/{total}")
        if elapsed is not None: self.time_label.config(text=f"Tempo: {elapsed:.1f}s")
        if message is not None: self.status_label.config(text=message)
        if color: self.status_bar.config(style=f"{color.capitalize()}.TFrame")
        else: self.status_bar.config(style="TFrame")

    def run_warnsdorff(self):
        self._update_status(message="Executando Warnsdorff...", color="yellow"); self.root.update_idletasks()
        self.path = warnsdorff_tour(self.n, self.start_idx); is_solution = len(self.path)==self.n*self.n
        msg = "Solução encontrada!" if is_solution else f"Caminho parcial com {len(self.path)} passos."; self._update_status(message=f"Warnsdorff: {msg}", color=None); self.animate_path(self.path, is_solution)

    def run_backtracking(self):
        self._update_status(message="Executando Backtracking...", color="yellow"); self.root.update_idletasks()
        self.path = backtracking_tour(self.n, self.start_idx)
        if self.path: self._update_status(message="Backtracking: Solução encontrada!", color=None); self.animate_path(self.path, True)
        else: self._update_status(message="Backtracking não encontrou solução no tempo limite.", color=None)

    def reset(self):
        if self.ga_state != 'idle' or self.animation_state != 'idle': return
        self.path=[]; self.ga=None; self.elapsed_time_paused=0; self.animation_state='idle'; self.last_hover_idx=-1
        self.pause_anim_btn.config(state=tk.DISABLED); self._update_status(gen='-', fitness='-', total='-', elapsed=0.0, message="Pronto.", color=None)
        if MATPLOTLIB_AVAILABLE: self.init_ga_graph(); self.redraw_canvas()

    def toggle_ga_run(self):
        if self.ga_state == 'idle':
            pop=int(self.pop_spin.get()); mut=float(self.mut_spin.get()); self.ga=GeneticKnightTour(self.n,pop,mut,GA_TOURN); self.ga.init_population(self.start_idx)
            self.ga_state='running'; self.run_ga_btn.config(text="Pausar GA"); self._toggle_controls(tk.DISABLED); self.start_time=time.time(); self.ga_loop()
        elif self.ga_state == 'running': self.ga_state='paused'; self.elapsed_time_paused=time.time()-self.start_time; self.run_ga_btn.config(text="Continuar GA"); self._update_status(color="yellow", message="GA Pausado.")
        elif self.ga_state == 'paused': self.ga_state='running'; self.run_ga_btn.config(text="Pausar GA"); self.start_time=time.time()-self.elapsed_time_paused; self.ga_loop()

    def ga_loop(self):
        if self.ga_state != 'running':
            if self.ga_state == 'idle': self._toggle_controls(tk.NORMAL); self.run_ga_btn.config(text="Iniciar GA")
            return
        solution_found = self.ga.step()
        self.path = self.ga.best_path[:] if self.ga.best_path else []
        self.redraw_canvas()
        max_fitness = self.n*self.n-1; elapsed = time.time()-self.start_time
        self._update_status(gen=self.ga.generation, fitness=self.ga.best_fitness, total=max_fitness, elapsed=elapsed, message="GA em execução...", color="yellow")
        if MATPLOTLIB_AVAILABLE and (self.ga.generation % 5 == 0 or solution_found): self.update_ga_graph()
        if solution_found or self.ga.generation >= GA_GEN_LIMIT:
            self.ga_state = 'idle'; msg = "SOLUÇÃO PERFEITA encontrada!" if solution_found else "Limite de gerações atingido."
            self._update_status(message=msg, color=None); self.animate_path(self.path, is_solution=solution_found)
        if self.ga_state == 'running': self.root.after(1, self.ga_loop)

    def init_ga_graph(self):
        self.ax_graph.clear(); self.ax_graph.set_title("Convergência do GA"); self.ax_graph.set_xlabel("Geração"); self.ax_graph.set_ylabel("Aptidão")
        self.ax_graph.grid(True, linestyle='--', alpha=0.6); self.fig.tight_layout(); self.graph_canvas.draw()

    def update_ga_graph(self):
        self.ax_graph.clear(); self.ax_graph.grid(True, linestyle='--', alpha=0.6)
        self.ax_graph.plot(self.ga.avg_fitness_history, label='Aptidão Média', color='deepskyblue')
        self.ax_graph.plot(self.ga.best_fitness_history, label='Melhor Aptidão', color='darkorange', linewidth=2)
        self.ax_graph.legend(); self.ax_graph.set_title("Convergência do GA"); self.ax_graph.set_xlabel("Geração"); self.ax_graph.set_ylabel("Aptidão")
        self.fig.tight_layout(); self.graph_canvas.draw()


# ----------------------------
# Executa app
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Apresentação Passeio do Cavalo — por Luiz, Marco, Maria e Vinicius")
    
    if not MATPLOTLIB_AVAILABLE:
        root.withdraw()
        tk.messagebox.showerror("Bibliotecas Faltando",
                                "As bibliotecas 'matplotlib' e/ou 'sv-ttk' não foram encontradas.\n\n"
                                "Por favor, instale-as com o comando:\n"
                                "pip install matplotlib sv-ttk\n\n"
                                "O programa será encerrado.")
        exit()

    sv_ttk.set_theme("dark") # Define o tema moderno (dark ou light)
    
    # Estilos para a barra de status colorida
    style = ttk.Style()
    style.configure("Green.TFrame", background="darkgreen")
    style.configure("Yellow.TFrame", background="#8B8000") # Dark Yellow

    root.state('zoomed')
    app = KnightTourGUI(root, n=BOARD_SIZE)

    root.mainloop()
