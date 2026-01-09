# Sigandwa User Guide - Visualizations & Features

## Quick Start Guide

### 1. Dashboard Overview
Access comprehensive system statistics and visualizations at `/`

**Features**:
- **Statistics Cards**: Key metrics (events, patterns, prophecies, relationships)
- **Risk Assessment**: Current civilization risk level with visual indicator
- **Charts**:
  - Events by Era (Bar Chart)
  - Event Type Distribution (Pie Chart)
  - Timeline Distribution (Area Chart)
  - Pattern Analysis (Line Chart)
- **System Status**: Backend service health checks

**Mobile**: All charts scroll horizontally on small screens

---

### 2. Interactive Timeline (`/timeline`)

#### Viewing the Timeline
- **Default View**: List of all 96 chronological events
- **D3 Visualization**: Toggle "Show Visualization" for interactive timeline

#### Controls
```
Zoom In     : Click + button or scroll wheel up
Zoom Out    : Click - button or scroll wheel down
Pan         : Click and drag the timeline
Reset View  : Click reset button
Export      : Download timeline as SVG
```

#### Event Details
- **Hover**: View quick tooltip
- **Click**: Open detailed modal with full information

#### Filtering
- **Search**: Type keywords to find events
- **Era Filter**: Select specific historical period
- **Type Filter**: Choose event type (Creation, Judgment, etc.)
- **Clear**: Reset all filters

#### Export Options
- **SVG**: Vector format for print/editing

---

### 3. Pattern Analysis (`/patterns`)

#### Viewing Patterns
- **Card View**: 6 pattern templates displayed
- **Click Card**: Open detailed analysis modal

#### Pattern Details
- Name and type
- Description
- Preconditions (warning signs)
- Typical outcomes
- Historical instances
- Timeline duration
- Confidence score
- Pattern evolution graph

#### Export Options
- **CSV**: Spreadsheet format
- **JSON**: Raw data format

**Mobile Tip**: Export buttons show icons only on small screens

---

### 4. Graph Network Analysis (`/graph`)

#### Interactive Network
- **108+ Nodes**: Events (blue), Patterns (green), Prophecies (purple)
- **Relationships**: Visual connections between nodes

#### Controls
```
Zoom In       : Click + button
Zoom Out      : Click - button
Fit to Screen : Click maximize button
Stabilize     : Re-run physics simulation
Search        : Filter nodes by name
Filter        : Show only specific node types
```

#### Interactions
- **Drag Nodes**: Reorganize network layout
- **Click Node**: View detailed information
- **Hover**: See node labels

#### Export Options
- **PNG**: Screenshot of current view

#### Advanced Features
- **Path Finder**: Find shortest connection between two events
- **Influential Events**: Top 10 most connected nodes
- **Event Chains**: Sequential event relationships
- **Prophecy Networks**: Prophecy-fulfillment connections

---

### 5. Global Search

#### Opening Search
- **Keyboard**: Press `⌘K` (Mac) or `Ctrl+K` (Windows/Linux)
- **Mouse**: Click "Search..." button in sidebar

#### Using Search
1. Type your query
2. Results appear instantly, grouped by:
   - Events (blue)
   - Patterns (green)
   - Prophecies (purple)
3. Click any result to navigate to that section

#### Search Tips
- Searches across: names, descriptions, actors, references
- Fuzzy matching: "crea" finds "Creation"
- Case insensitive
- Shows top 5 results per category

#### Keyboard Shortcuts
```
⌘K / Ctrl+K  : Open search
↑ ↓          : Navigate results
Enter        : Select result
Esc          : Close search
```

---

### 6. Prophecy Tracking (`/prophecies`)

#### Features
- View all tracked prophecies
- Fulfillment timeline
- Confidence scores
- Category filtering
- Detailed text and analysis

---

### 7. Simulation Dashboard (`/simulation`)

#### Risk Assessment
- 25 world indicators
- Risk level calculation
- Scenario projections
- Historical analog matching

---

## Export Guide

### CSV Export
**Best for**: Spreadsheet analysis, Excel, Google Sheets

**Contains**:
- All visible columns
- Properly escaped text
- Header row

**How to use**:
1. Click "CSV" button
2. File downloads automatically
3. Open in Excel or spreadsheet app

### JSON Export
**Best for**: Developers, data analysis, backup

**Contains**:
- Complete data structure
- All fields and metadata
- Pretty-printed format

**How to use**:
1. Click "JSON" button
2. File downloads automatically
3. Import into your application

### SVG Export (Timeline)
**Best for**: Print, presentations, editing

**How to use**:
1. View D3 timeline
2. Adjust zoom/pan to desired view
3. Click "Export SVG"
4. Edit in Illustrator/Inkscape if needed

### PNG Export (Graph)
**Best for**: Reports, documentation, sharing

**How to use**:
1. Arrange graph network as desired
2. Click "Export PNG"
3. Image saves current view

---

## Mobile Usage

### Best Practices
- **Rotate**: Use landscape for better chart viewing
- **Touch**: All controls are touch-optimized (44px targets)
- **Scroll**: Charts scroll horizontally on small screens
- **Pinch**: Zoom works in timeline and graph
- **Menu**: Use hamburger menu for navigation

### Mobile-Specific Features
- Responsive layouts adapt automatically
- Touch gestures for zoom/pan
- Optimized font sizes
- Icon-only buttons to save space
- Full-screen modals

---

## Performance Tips

### For Best Performance
1. **Use Filters**: Narrow down data before visualizing
2. **Stabilize Graph**: Click "Stabilize" if network is jumpy
3. **Clear Cache**: Refresh if data seems stale
4. **Close Modals**: Don't leave detail modals open

### Troubleshooting
- **Slow Timeline**: Try filtering to fewer events
- **Jumpy Graph**: Click "Stabilize" button
- **Charts Not Loading**: Check internet connection
- **Export Issues**: Ensure pop-ups are allowed

---

## Keyboard Shortcuts

### Global
```
⌘K / Ctrl+K     : Open global search
Esc             : Close modals/search
```

### Timeline
```
Scroll Wheel    : Zoom in/out
Click + Drag    : Pan timeline
```

### Graph
```
Click + Drag    : Move nodes
Scroll Wheel    : Zoom view
```

---

## Data Update Frequency

- **Events**: Static historical data
- **Patterns**: Updated when new instances detected
- **Prophecies**: Updated with new fulfillments
- **Risk Assessment**: Daily calculation
- **Graph**: Synced on page load (use "Sync Graph" to refresh)

---

## Browser Compatibility

### Recommended Browsers
- ✅ Chrome 90+ (Best performance)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Mobile Browsers
- ✅ Chrome Mobile
- ✅ Safari iOS
- ✅ Samsung Internet

### Requirements
- JavaScript enabled
- Cookies enabled (for session)
- Local storage (for preferences)

---

## Accessibility

### Features
- **Keyboard Navigation**: Full keyboard support
- **Focus Indicators**: Clear visual focus
- **Touch Targets**: 44px minimum size
- **Color Contrast**: WCAG AA compliant
- **Screen Readers**: Semantic HTML

### Keyboard Navigation
- `Tab`: Move forward
- `Shift+Tab`: Move backward
- `Enter`: Activate/select
- `Space`: Toggle buttons
- `Esc`: Close modals

---

## Support & Feedback

### Getting Help
- **Issues**: https://github.com/Eccb7/sigandwa/issues
- **Discussions**: https://github.com/Eccb7/sigandwa/discussions
- **Documentation**: Check `/docs` folder

### Reporting Bugs
Include:
1. Browser and version
2. Device type (desktop/mobile)
3. Steps to reproduce
4. Expected vs actual behavior
5. Screenshots if applicable

---

## Tips & Tricks

### Power User Tips
1. **Bookmark Views**: Use browser bookmarks for frequent filters
2. **Export Regularly**: Download data for offline analysis
3. **Combine Filters**: Use multiple filters simultaneously
4. **Save Searches**: Note useful search terms
5. **Learn Shortcuts**: Master ⌘K for speed

### Data Analysis Workflow
1. Start with Dashboard for overview
2. Use Global Search to find specific items
3. Dive into Timeline for chronological context
4. Check Patterns for recurring themes
5. Explore Graph for relationships
6. Export data for deeper analysis

---

## Version Information

- **Current Version**: v0.7.0
- **Last Updated**: January 9, 2026
- **Phase**: 7 Complete (Advanced Visualizations)
- **Next Release**: Q4 2026 (Authentication & Beta)

---

**Questions?** Check the [full documentation](https://github.com/Eccb7/sigandwa/tree/main/docs) or [open an issue](https://github.com/Eccb7/sigandwa/issues).
