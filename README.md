# EBVCubeVisualizer                                                <img align="left" src="https://github.com/E-O-Conchas/EBVCubeVisualizerPlugin/blob/master/EBVIcon.png" alt="drawing" width="100"/>      

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
     
2. **Plugin Interface Overview:**
   - The plugin interface consists of three main sections:
     
     - _Dataset Explorer:_ Located on the left, it displays the hierarchical structure of the loaded dataset, including scenarios, metrics, and EBV data cubes.
     - _Attributes Panel:_ Positioned on the top-right, it dinamically updates to show the attributes of the selected data set, scenario, metric or EBV data cube
     - _Map Panel:_ Found on the buttom-rigth, it allows users to select specific parameters (e.g., Scenario, Metric, Entity, and Time) and visualize the data by clicking the `Add Layer` button

     *Below is an example of the plugin interface*
     
     <img src="https://github.com/user-attachments/assets/abbf4778-d74e-4432-8a08-f85e5ec193e1" width="650"/>


4. **Load a netCDF File:**
   - Use the file browser to select a EBVCube netCDF file.
   - Once loaded, the structure of the dataset is displayed in the **Dataset Explorer** on the left, showing scnenarios (if available), metrics and the ebv data cube.

     *Example of the loaded dataset*

     <img src="https://github.com/user-attachments/assets/fb150dec-69cc-4515-97da-772d2ea4548e" width="650"/>

5. **Explore the Hierarchical Structure of the Dataset**:
   - The **Dataset Explorer** displays the hierarchical structure, organized into:
     - File name: Represent the root of the dataset.
     - Scenarios (e.g., `scenario_1`): Represent different modeling or simulation scenarios in the dataset.
     - Metrics (e.g., `metric_1`): Represent specific biodiversity measurements or calculations.
     - Ebv data cube: Represent the four-dimensional data cube.

   - To view details:
     - File name: Click to display the global attributes of the data set (e.g., `doi`, `summary`, `project_name`, `data_created`)
     - Scenarios: Click to view associated attributes (e.g., `standard_name`, `long_name`).
     - Metric: Click to see specific attributes (e.g., `standard_name`, `long_name`, `units`).
     - Ebv data cube: Click to explore its attibures (e.g., `units`, `FillValue`, `long_name`, ` coverage_content_type`)
       
      *Example of attributes displayed when you click 'mteric_1'*
     
     <img src="https://github.com/user-attachments/assets/a4e7e607-b9d8-4dde-8cae-c0ed92ce0e4a" width="650"/>

   - **Tip**: The attributes panel updates dynamically based on your selection in the **Dataset Explorer**.

6. **Select Parameters:**
   - Use the dropdown menus under **Map Panel** to select:
       - `Entity`: e.g., species like *Hyla arborea*.
       - `Time`: e.g., 2020-01-01.
       - `Metric`: e.g., Biodiversity metric such as *Weighted Mean habitat suitability*.
       - `Scenario`: e.g., SSP1 (if available).

       *Example of selecting parameters*
       
      <img src="https://github.com/user-attachments/assets/94271659-116f-401f-b321-22f15d40ef60" width="400"/>

7. **Visualize Data:**
   - Click the `Add Layer` button to display the selected subset of data on the QGIS canvas. 
   - The layer will include an automatically generated color ramp based on the data values.
   
      *Example of a visualized layer on the QGIS canvas*

      <img src="https://github.com/user-attachments/assets/3578f1f0-d465-47d7-b0b9-0b00a5d1058e" width="900"/>

8. **Customize Visualization:**
   - Use QGIS layer properties to further refine the visualization:
     - Adjust the color ramp for better interpretation.
     - Apply spatial analysis tools for advanced exploration.

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

## Example Dataset

The examples in this README use the publicly available dataset entitled **"Species habitat suitability of European terrestrial vertebrates for contemporary climate and land use"**, provided by the EBV Data Portal. It is stored as an EBVCube netCDF file and can be accessed directly through the following link:

- **EBV Data Portal Link**: [Species habitat suitability of European terrestrial vertebrates for contemporary climate and land use](https://portal.geobon.org/ebv-detail?id=84&v=1)

This dataset serves as an example to showcase the functionality of the plugin. You are encouraged to explore additional datasets available on the [EBV Data Portal](https://portal.geobon.org/datasets) for your analyses.

## Contributing

We welcome contributions to this project! If you have an idea for a new feature or have found a bug, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Enhancements
 
- **User Interface Improvements:** Implement new features to enhance the user experience and make the plugin more intuitive.
- **Data Availability:** Integrate the EBV Portal catalog within the plugin to facilitate data retrieval.

Stay tuned for future updates and enhancements!
````
