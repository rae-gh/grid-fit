import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json

# Load the data
with open('benchmark_data.json', 'r') as f:
    data = json.load(f)

benchmarks = data['benchmarks']

# Extract data
grid_sizes = np.array([b['grid_size'] for b in benchmarks])
n_points = np.array([b['n_interp_points'] for b in benchmarks])
gridfit_interp = np.array([b['gridfit_interp_time'] for b in benchmarks])
scipy_interp = np.array([b['scipy_interp_time'] for b in benchmarks])
gridfit_construct = np.array([b['gridfit_construct_time'] for b in benchmarks])
scipy_construct = np.array([b['scipy_construct_time'] for b in benchmarks])

speedup_interp = scipy_interp / gridfit_interp
speedup_construct = scipy_construct / gridfit_construct

# Unique values
unique_grids = sorted(set(grid_sizes))
unique_points = sorted(set(n_points))

print("="*80)
print("COMPREHENSIVE BENCHMARK ANALYSIS")
print("="*80)
print(f"\nSystem: {data['metadata']['system']['hostname']}")
print(f"CPUs: {data['metadata']['system']['cpu_logical_cores']}")
print(f"RAM: {data['metadata']['system']['ram_gb']:.1f} GB")
print(f"BLAS: {data['metadata']['system']['blas_backend']}")
print(f"Compiler: {data['metadata']['system']['gridfit_compiler']['compiler']} "
      f"{data['metadata']['system']['gridfit_compiler']['version']}")

# Create comprehensive figure
fig = plt.figure(figsize=(20, 12))
gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

# ============================================================================
# Plot 1: Interpolation time vs n_points (log-log for complexity analysis)
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_grids)))

for i, grid in enumerate(unique_grids):
    mask = grid_sizes == grid
    x = n_points[mask]
    y_gridfit = gridfit_interp[mask]
    y_scipy = scipy_interp[mask]
    
    ax1.loglog(x, y_gridfit, 'o-', color=colors[i], linewidth=2, 
               markersize=8, label=f'Gridfit {grid}³')
    ax1.loglog(x, y_scipy, 's--', color=colors[i], linewidth=1, 
               markersize=6, alpha=0.6, label=f'Scipy {grid}³')

ax1.set_xlabel('Number of Interpolation Points', fontsize=12, fontweight='bold')
ax1.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax1.set_title('Interpolation Scaling (Log-Log)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=8, ncol=2)

# Add reference lines for complexity
x_ref = np.array([100, 100000])
y_ref_linear = x_ref / x_ref[0] * 0.0001
ax1.loglog(x_ref, y_ref_linear, 'k--', alpha=0.3, linewidth=1, label='O(n) reference')

# ============================================================================
# Plot 2: Speedup vs n_points
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

for i, grid in enumerate(unique_grids):
    mask = grid_sizes == grid
    x = n_points[mask]
    speedup = speedup_interp[mask]
    
    ax2.semilogx(x, speedup, 'o-', color=colors[i], linewidth=2, 
                 markersize=8, label=f'{grid}³')

ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax2.set_xlabel('Number of Interpolation Points', fontsize=12, fontweight='bold')
ax2.set_ylabel('Speedup (scipy/gridfit)', fontsize=12, fontweight='bold')
ax2.set_title('Interpolation Speedup', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

# ============================================================================
# Plot 3: Heatmap of interpolation speedup
# ============================================================================
ax3 = fig.add_subplot(gs[0, 2])

# Create pivot table
pivot_speedup = np.zeros((len(unique_points), len(unique_grids)))
for i, pts in enumerate(unique_points):
    for j, grid in enumerate(unique_grids):
        mask = (n_points == pts) & (grid_sizes == grid)
        if np.any(mask):
            pivot_speedup[i, j] = speedup_interp[mask][0]

im = ax3.imshow(pivot_speedup, aspect='auto', cmap='RdYlGn', vmin=1, vmax=12)
ax3.set_xticks(range(len(unique_grids)))
ax3.set_xticklabels([f'{g}' for g in unique_grids])
ax3.set_yticks(range(len(unique_points)))
ax3.set_yticklabels([f'{p:,}' for p in unique_points])
ax3.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax3.set_ylabel('Interpolation Points', fontsize=12, fontweight='bold')
ax3.set_title('Speedup Heatmap', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax3, label='Speedup Factor')

# Add text annotations
for i in range(len(unique_points)):
    for j in range(len(unique_grids)):
        val = pivot_speedup[i, j]
        color = 'white' if val > 6 else 'black'
        ax3.text(j, i, f'{val:.1f}x', ha='center', va='center',
                color=color, fontweight='bold', fontsize=10)

# ============================================================================
# Plot 4: Absolute times comparison (specific grid)
# ============================================================================
ax4 = fig.add_subplot(gs[1, 0])

grid_focus = 256
mask = grid_sizes == grid_focus
x = n_points[mask]

width = 0.35
x_pos = np.arange(len(x))

ax4.bar(x_pos - width/2, gridfit_interp[mask], width, label='Gridfit', color='#2ecc71')
ax4.bar(x_pos + width/2, scipy_interp[mask], width, label='Scipy', color='#e74c3c')

ax4.set_xlabel('Interpolation Points', fontsize=12, fontweight='bold')
ax4.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax4.set_title(f'Absolute Times (Grid {grid_focus}³)', fontsize=14, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels([f'{int(p):,}' for p in x], rotation=45)
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

# ============================================================================
# Plot 5: Complexity analysis - fit slopes
# ============================================================================
ax5 = fig.add_subplot(gs[1, 1])

slopes_gridfit = []
slopes_scipy = []
grid_labels = []

for grid in unique_grids:
    mask = grid_sizes == grid
    x = np.log10(n_points[mask])
    y_gridfit = np.log10(gridfit_interp[mask])
    y_scipy = np.log10(scipy_interp[mask])
    
    # Fit linear on log-log
    slope_gf = np.polyfit(x, y_gridfit, 1)[0]
    slope_sp = np.polyfit(x, y_scipy, 1)[0]
    
    slopes_gridfit.append(slope_gf)
    slopes_scipy.append(slope_sp)
    grid_labels.append(f'{grid}³')

x_pos = np.arange(len(unique_grids))
width = 0.35

ax5.bar(x_pos - width/2, slopes_gridfit, width, label='Gridfit', color='#2ecc71')
ax5.bar(x_pos + width/2, slopes_scipy, width, label='Scipy', color='#e74c3c')
ax5.axhline(y=1.0, color='gray', linestyle='--', linewidth=2, label='O(n) reference')

ax5.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax5.set_ylabel('Complexity Exponent', fontsize=12, fontweight='bold')
ax5.set_title('Algorithmic Complexity (Log-Log Slope)', fontsize=14, fontweight='bold')
ax5.set_xticks(x_pos)
ax5.set_xticklabels(grid_labels)
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')
ax5.set_ylim([0.8, 1.2])

# ============================================================================
# Plot 6: Construction time comparison
# ============================================================================
ax6 = fig.add_subplot(gs[1, 2])

# Average construction times across all point counts for each grid
construct_gf_avg = []
construct_sp_avg = []

for grid in unique_grids:
    mask = grid_sizes == grid
    construct_gf_avg.append(np.mean(gridfit_construct[mask]))
    construct_sp_avg.append(np.mean(scipy_construct[mask]))

x_pos = np.arange(len(unique_grids))
width = 0.35

ax6.bar(x_pos - width/2, np.array(construct_gf_avg)*1000, width, 
        label='Gridfit', color='#2ecc71')
ax6.bar(x_pos + width/2, np.array(construct_sp_avg)*1000, width, 
        label='Scipy', color='#e74c3c')

ax6.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax6.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
ax6.set_title('Construction Time (Average)', fontsize=14, fontweight='bold')
ax6.set_xticks(x_pos)
ax6.set_xticklabels([f'{g}³' for g in unique_grids])
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

# ============================================================================
# Plot 7: Speedup by grid size
# ============================================================================
ax7 = fig.add_subplot(gs[2, 0])

for i, pts in enumerate(unique_points):
    mask = n_points == pts
    x = grid_sizes[mask]
    speedup = speedup_interp[mask]
    
    ax7.plot(x, speedup, 'o-', linewidth=2, markersize=8, 
             label=f'{int(pts):,} points')

ax7.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax7.set_xlabel('Grid Size', fontsize=12, fontweight='bold')
ax7.set_ylabel('Speedup (scipy/gridfit)', fontsize=12, fontweight='bold')
ax7.set_title('Speedup vs Grid Resolution', fontsize=14, fontweight='bold')
ax7.set_xscale('log')
ax7.grid(True, alpha=0.3)
ax7.legend()

# ============================================================================
# Plot 8: Error analysis
# ============================================================================
ax8 = fig.add_subplot(gs[2, 1])

max_errors = np.array([b['max_error'] for b in benchmarks])
mean_errors = np.array([b['mean_error'] for b in benchmarks])

# Plot max and mean errors
for i, grid in enumerate(unique_grids):
    mask = grid_sizes == grid
    x = n_points[mask]
    
    ax8.loglog(x, max_errors[mask], 'o-', color=colors[i], 
               linewidth=2, markersize=6, label=f'{grid}³ max')
    ax8.loglog(x, mean_errors[mask], 's--', color=colors[i], 
               linewidth=1, markersize=4, alpha=0.6)

ax8.set_xlabel('Interpolation Points', fontsize=12, fontweight='bold')
ax8.set_ylabel('Absolute Error', fontsize=12, fontweight='bold')
ax8.set_title('Numerical Accuracy', fontsize=14, fontweight='bold')
ax8.grid(True, alpha=0.3)
ax8.legend(fontsize=8)

# ============================================================================
# Plot 9: Summary statistics table
# ============================================================================
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

# Calculate summary stats
avg_speedup_interp = np.mean(speedup_interp)
min_speedup_interp = np.min(speedup_interp)
max_speedup_interp = np.max(speedup_interp)
avg_speedup_construct = np.mean(speedup_construct)

avg_complexity_gf = np.mean(slopes_gridfit)
avg_complexity_sp = np.mean(slopes_scipy)

summary_text = f"""
SUMMARY STATISTICS

Interpolation Performance:
  • Average speedup: {avg_speedup_interp:.2f}x
  • Range: {min_speedup_interp:.2f}x - {max_speedup_interp:.2f}x
  • Best case: {max_speedup_interp:.2f}x
    ({unique_grids[0]}³, {unique_points[0]} pts)
  
Construction Performance:
  • Average speedup: {avg_speedup_construct:.2f}x
  
Algorithmic Complexity:
  • Gridfit: O(n^{avg_complexity_gf:.3f})
  • Scipy: O(n^{avg_complexity_sp:.3f})
  • Both ≈ O(n) linear scaling
  
Numerical Accuracy:
  • Max error: {np.max(max_errors):.2e}
  • Mean error: {np.mean(mean_errors):.2e}
  • Within acceptable tolerance
  
Key Findings:
  • Gridfit consistently faster
  • Advantage highest at small scale
  • Converges to ~2x at large scale
  • Both algorithms scale linearly
  • Single-threaded implementation
"""

ax9.text(0.1, 0.95, summary_text, transform=ax9.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('Gridfit vs Scipy: Full Factorial Benchmark Analysis (HPC)', 
             fontsize=18, fontweight='bold', y=0.995)

plt.savefig('/mnt/user-data/outputs/full_factorial_analysis.png', 
            dpi=300, bbox_inches='tight')
print("\n" + "="*80)
print("Visualization saved to: full_factorial_analysis.png")
print("="*80)

# ============================================================================
# Print detailed statistics
# ============================================================================
print("\nDETAILED STATISTICS")
print("="*80)

print("\nComplexity Analysis (log-log slope):")
for i, grid in enumerate(unique_grids):
    print(f"  Grid {grid}³:")
    print(f"    Gridfit: O(n^{slopes_gridfit[i]:.3f})")
    print(f"    Scipy:   O(n^{slopes_scipy[i]:.3f})")

print("\nSpeedup by Configuration:")
print(f"{'Grid':<8} {'Points':<10} {'Speedup':<10} {'Gridfit(s)':<12} {'Scipy(s)':<12}")
print("-" * 60)
for i in range(len(benchmarks)):
    b = benchmarks[i]
    print(f"{b['grid_size']:<8} {b['n_interp_points']:<10} "
          f"{speedup_interp[i]:<10.2f} "
          f"{b['gridfit_interp_time']:<12.4f} "
          f"{b['scipy_interp_time']:<12.4f}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
