import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Benchmark data
data = [
    # Grid, Samples, Interp_speedup, Construct_speedup
    [50, 500, 5.12, 4.38],
    [100, 500, 5.15, 3.16],
    [200, 500, 5.67, 3.08],
    [256, 500, 1.72, 3.93],
    [384, 500, 2.99, 2.42],
    [512, 500, 2.82, 2.21],
    [1024, 500, 2.83, 6.58],
    [50, 1000, 2.34, 1.53],
    [100, 1000, 2.23, 4.11],
    [200, 1000, 2.06, 5.48],
    [256, 1000, 1.97, 5.76],
    [384, 1000, 1.79, 8.98],
    [512, 1000, 1.75, 7.85],
    [1024, 1000, -1.10, 3.80],  # scipy faster for interp
    [50, 10000, 1.49, 3.18],
    [100, 10000, 1.46, 3.27],
    [200, 10000, 1.54, 3.36],
    [256, 10000, 1.27, 3.29],
    [384, 10000, 1.45, 2.87],
    [512, 10000, 1.32, 4.78],
    [1024, 10000, 1.65, 18.46],
    [50, 100000, 1.67, 3.55],
    [100, 100000, 1.49, 3.46],
    [200, 100000, 1.26, 2.32],
    [256, 100000, 1.31, 2.78],
    [384, 100000, 1.17, 3.25],
    [512, 100000, 1.61, 4.60],
    [1024, 100000, 1.47, 4.23],
]

data = np.array(data)
grid_sizes = data[:, 0]
samples = data[:, 1]
interp_speedup = data[:, 2]
construct_speedup = data[:, 3]

# Separate by sample count
sample_counts = [500, 1000, 10000, 100000]
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
markers = ['o', 's', '^', 'd']

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Plot 1: Interpolation speedup vs grid size
ax1 = fig.add_subplot(gs[0, 0])
for i, sc in enumerate(sample_counts):
    mask = samples == sc
    ax1.plot(grid_sizes[mask], interp_speedup[mask], 
             marker=markers[i], linewidth=2, markersize=8,
             label=f'{sc:,} samples', color=colors[i])

ax1.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax1.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax1.set_ylabel('Speedup Factor (gridfit/scipy)', fontsize=12, fontweight='bold')
ax1.set_title('Interpolation Performance', fontsize=14, fontweight='bold')
ax1.set_xscale('log')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='best')
ax1.text(0.02, 0.02, 'Below 1.0 = scipy faster', transform=ax1.transAxes,
         fontsize=9, verticalalignment='bottom', color='gray', style='italic')

# Plot 2: Construction speedup vs grid size
ax2 = fig.add_subplot(gs[0, 1])
for i, sc in enumerate(sample_counts):
    mask = samples == sc
    ax2.plot(grid_sizes[mask], construct_speedup[mask], 
             marker=markers[i], linewidth=2, markersize=8,
             label=f'{sc:,} samples', color=colors[i])

ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax2.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax2.set_ylabel('Speedup Factor (gridfit/scipy)', fontsize=12, fontweight='bold')
ax2.set_title('Construction Performance', fontsize=14, fontweight='bold')
ax2.set_xscale('log')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='best')

# Plot 3: Heatmap of interpolation speedup
ax3 = fig.add_subplot(gs[1, 0])
pivot_interp = np.zeros((len(sample_counts), 7))
for i, sc in enumerate(sample_counts):
    mask = samples == sc
    pivot_interp[i, :] = interp_speedup[mask]

im1 = ax3.imshow(pivot_interp, aspect='auto', cmap='RdYlGn', vmin=0, vmax=6)
ax3.set_xticks(range(7))
ax3.set_xticklabels(['50', '100', '200', '256', '384', '512', '1024'])
ax3.set_yticks(range(4))
ax3.set_yticklabels([f'{sc:,}' for sc in sample_counts])
ax3.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax3.set_ylabel('Sample Count', fontsize=12, fontweight='bold')
ax3.set_title('Interpolation Speedup Heatmap', fontsize=14, fontweight='bold')
plt.colorbar(im1, ax=ax3, label='Speedup Factor')

# Add values to heatmap
for i in range(len(sample_counts)):
    for j in range(7):
        val = pivot_interp[i, j]
        color = 'white' if val > 3 else 'black'
        ax3.text(j, i, f'{val:.2f}', ha='center', va='center', 
                color=color, fontweight='bold', fontsize=9)

# Plot 4: Heatmap of construction speedup
ax4 = fig.add_subplot(gs[1, 1])
pivot_construct = np.zeros((len(sample_counts), 7))
for i, sc in enumerate(sample_counts):
    mask = samples == sc
    pivot_construct[i, :] = construct_speedup[mask]

im2 = ax4.imshow(pivot_construct, aspect='auto', cmap='RdYlGn', vmin=0, vmax=10)
ax4.set_xticks(range(7))
ax4.set_xticklabels(['50', '100', '200', '256', '384', '512', '1024'])
ax4.set_yticks(range(4))
ax4.set_yticklabels([f'{sc:,}' for sc in sample_counts])
ax4.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax4.set_ylabel('Sample Count', fontsize=12, fontweight='bold')
ax4.set_title('Construction Speedup Heatmap', fontsize=14, fontweight='bold')
plt.colorbar(im2, ax=ax4, label='Speedup Factor')

# Add values to heatmap
for i in range(len(sample_counts)):
    for j in range(7):
        val = pivot_construct[i, j]
        color = 'white' if val > 5 else 'black'
        ax4.text(j, i, f'{val:.1f}', ha='center', va='center', 
                color=color, fontweight='bold', fontsize=9)

plt.suptitle('Gridfit vs SciPy Performance Comparison', 
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig('benchmark_analysis.png', dpi=300, bbox_inches='tight')
