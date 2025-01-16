# EBVCubeVisualizer                                                <img align="left" src="https://github.com/E-O-Conchas/EBVCubeVisualizerPlugin/blob/master/EBVIcon.png" alt="drawing" width="80"/>      

**EBVCubeVisualizer** is a QGIS plugin tailored for exploring Essential Biodiversity Variables (EBVs) stored in the [EBV Data Portal](https://portal.geobon.org/datasets) as EBVCube netCDF files. This plugin enables users to extract and visualize specific slices of EBV data cubes, allowing flexible selection based on *time*, *entity*, *scenario*, and *metric*. While not designed for in-depth biodiversity analysis, EBVCubeVisualizer serves as a powerful and intuitive starting point for exploring datasets and preparing data for further analysis.

## Features

- *Load and Visualize EBVCube Data:* Seamlessly load EBVCube dataset stored in netCDF format and visualize them directly in QGIs.
- *Flexible Data Subsetting:* Extract specific slices of data by selecting time, entity, scenario, and metric, providing targeted views of biodiversity information.
- *Metadata and Data Structure Discovery:* Explore the full metadata and hierarchical strcuture of EBVCube datasets, making it easier to understand and navigate complex biodiversity data.
- *Automatic CRS Application:* Automatically apply the correct Coordinate Refrence System (CRS) based on the metadata embedded in the netCDF files. 
- *Clear and Informative Layer Naming:* Display selected data on the QGIS canvas with meaningful layer names that incorporate entity and time details for easy identification.

## Installation

1. Download this repository as zip file.
2. Open QGIS and go to `Plugins > Manage and Install Plugins...`.
3. Click on `Install from ZIP` and select the downloaded file.
4. Activate the plugin by checking the box next to "EBVCubeVisualizerPlugin" in the `Installed` tab.

## Usage

1. **Open the Plugin:**
   - After installation, go to `Plugins > EBVCubeVisualizer` to open the plugin interface.

     *Below is an example of the plugin interface:*
     
     <img src="https://github.com/user-attachments/assets/350c1045-8b4e-409a-a1f2-1dbe89e8574b" width="650"/>
     

3. **Load a netCDF File:**
   - Use the file browser to select a netCDF file containing EBVCube data.
   - Once loaded, the structure of the dataset is displayed in the **Tree Widget** on the left, showing groups (e.g. metrics) and their variables (e.g. 'ebv_cube')

     *Example of the loaded dataset*

     <img src="https://github.com/user-attachments/assets/75665bb8-95e0-436d-9493-3a4a26bc5b47" width="650"/>

4. **Explore the Dataset Structure**:
   - The **Dataset Explorer** shows the hierarchy of the dataset:
     - **Parent Nodes** (e.g., `scenario_1`, `metric_1`): Represent groups in the dataset.
     - **Child Nodes** (e.g., `ebv_cube`): Represent variables or specific data items within each group.

   - To view details, click on:
     - **Parent Nodes** to display group-level attributes (e.g., `long_name`, `standard_name`, `units`).
     - **Child Nodes** to display variable-specific attributes (e.g., `units`, `FillValue`, ` coverage_content_type`).

     <img src="https://github.com/user-attachments/assets/75665bb8-95e0-436d-9493-3a4a26bc5b47" width="650"/>

   - **Tip**: The attribute panel on the right updates dynamically based on your selection in the tree widget.


5. **Select Parameters:**!
   - Choose the desired `Entity`(e.g., species), `Time`(e.g., year), `Metric` (e.g., Biodiversity metric) and `Scenario` (e.g., SSP1) from the dropdown menus.
6. **Visualize Data:**
   - Click the `Add Layer` button to display the selected subset of data on the QGIS canvas. The layer will be styled with an automatically generated color ramp base on the data values.
7. **Customize Visualization:**
   - Use QGIS layer properties to further customize the visualization, such as adjusting the color scheme or applaying spatial analysis tools.

## Dependencies

- QGIS 3.0 or later
- Python 3.6 or later
- Required Python Libraries:
  - `netCDF4`: Handles netCDF file loading and data extraction.
  - `numpy`: Supports array operations and data handling.
  - `gdal`: Facilitates raster data management and processing.

if you encounter issues with missing libraries, follow the instructions below to install them:

### Installing Libraries via OSGeo4W Shell

1. Open the **OSGeo4W Shell**.
2. Run the following commands to install the required libraries:
   ```bash
   python -m pip install netCDF4 numpy gdal

3. Restart QGIS to ensure the new libraries are recognized

## Troubleshooting

If you encounter any issues with the plugin, please follow these steps:

1. Ensure that all dependencies are installed and correctly configured.
2. Verify that the netCDF file you are using is properly formatted and contains the required dimensions (e.g., `entity`, `time`, `lat`, `lon`).
3. Check the QGIS Python console for any error messages and provide them when seeking help.

## Contributing

We welcome contributions to this project! If you have an idea for a new feature or have found a bug, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Enhancements
 
- **User Interface Improvements:** Implement new features to enhance the user experience and make the plugin more intuitive.
- **Data Availability:** Integrate the EBV Portal catalog within the plugin to facilitate data retrieval.

Stay tuned for future updates and enhancements!
````
