# EBVCubeVisualizerPlugin                                                 <img src="https://github.com/E-O-Conchas/EBVCubeVisualizerPlugin/blob/master/EBVIcon.png" alt="drawing" width="50"/>      

**EBVCubeVisualizerPlugin** is a QGIS plugin designed for visualizing Essential Biodiversity Variables (EBVs) stored in [EBV portal](https://portal.geobon.org/home) as NetCDF files. The plugin allows users to select and display specific subsets of EBV data based on time, entity, scenario, and metric, providing a flexible and powerful tool for biodiversity analysis.

## Features

- Load and visualize EBV data stored in NetCDF files.
- Subset data by time, entity, scenario, and metric.
- Customize the visualization with color ramps and other display options.
- Automatically apply the correct Coordinate Reference System (CRS) based on the NetCDF file metadata.
- Display the selected data on the QGIS canvas with clear layer names that include entity and time information.

## Installation

1. Clone or download this repository.
2. Open QGIS and go to `Plugins > Manage and Install Plugins...`.
3. Click on `Install from ZIP` and select the downloaded file.
4. Activate the plugin by checking the box next to "EBVCubeVisualizerPlugin" in the `Installed` tab.

## Usage

1. **Open the Plugin:**
   - After installation, go to `Plugins > EBVCubeVisualizerPlugin` to open the plugin interface.

2. **Load a NetCDF File:**
   - Use the file browser to select a NetCDF file containing EBV data.

3. **Select Parameters:**
   - Choose the desired `Entity`, `Time`, `Scenario`, and `Metric` from the dropdown menus.

4. **Display Data:**
   - Click the `Add Layer` button to visualize the selected subset of data on the QGIS canvas.

5. **Customize Visualization:**
   - The plugin automatically applies a color ramp to the displayed data. You can further customize the visualization using the QGIS layer properties.

## Example Workflow

1. **Load the NetCDF File:**
   - Open the plugin and navigate to your NetCDF file. Load it into the plugin.
   
2. **Select Parameters:**
   - Choose the specific `Entity` (e.g., species), `Time` (e.g., year), `Scenario` (e.g., climate scenario), and `Metric` (e.g., biodiversity metric) that you want to visualize.

3. **Visualize Data:**
   - The selected subset will be displayed on the QGIS canvas with an automatically generated color ramp based on the data values.

4. **Explore and Analyze:**
   - Use QGIS tools to explore, analyze, and interpret the EBV data. Apply further QGIS functionality, such as spatial analysis or custom styling, to gain insights from the visualized data.

## Dependencies

- QGIS 3.0 or later
- Python 3.6 or later
- Required Python Libraries:
  - `netCDF4`: Handles NetCDF file loading and data extraction.
  - `numpy`: Supports array operations and data handling.
  - `gdal`: Facilitates raster data management and processing.
  - `matplotlib`: Used internally for plotting and data manipulation.

## Troubleshooting

If you encounter any issues with the plugin, please follow these steps:

1. Ensure that all dependencies are installed and correctly configured.
2. Verify that the NetCDF file you are using is properly formatted and contains the required dimensions (e.g., `entity`, `time`, `lat`, `lon`).
3. Check the QGIS Python console for any error messages and provide them when seeking help.
4. Refer to the plugin’s documentation and FAQs for common issues and solutions.

## Contributing

We welcome contributions to this project! If you have an idea for a new feature or have found a bug, feel free to open an issue or submit a pull request.

### How to Contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push your branch to GitHub: `git push origin feature-name`
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This plugin was developed using the QGIS Plugin Development framework.
- Special thanks to the QGIS and NetCDF communities for their support and resources.

## Future Enhancements

- **Expanded Data Sources:** Support for additional data formats beyond NetCDF.
- **Advanced Analysis Tools:** Integrate additional biodiversity metrics and analysis tools directly into the plugin.
- **User Interface Improvements:** Streamline the interface for easier parameter selection and data visualization.

Stay tuned for future updates and enhancements!

