<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" minScale="1e+08" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" version="3.24.2-Tisler">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" mode="0" fetchMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option name="WMSBackgroundLayer" type="bool" value="false"/>
      <Option name="WMSPublishDataSourceUrl" type="bool" value="false"/>
      <Option name="embeddedWidgets/count" type="int" value="0"/>
      <Option name="identify/format" type="QString" value="Value"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour" enabled="false" zoomedOutResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" opacity="1" classificationMin="-9.9112749" band="9" alphaBand="-1" classificationMax="19.6030865">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0" maximumValue="19.6030865" classificationMode="1" minimumValue="-9.9112749000000004" labelPrecision="6">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option name="color1" type="QString" value="17,116,177,255"/>
              <Option name="color2" type="QString" value="189,37,40,255"/>
              <Option name="direction" type="QString" value="cw"/>
              <Option name="discrete" type="QString" value="0"/>
              <Option name="rampType" type="QString" value="gradient"/>
              <Option name="spec" type="QString" value="rgb"/>
              <Option name="stops" type="QString" value="0.175481;118,185,169,255;rgb;ccw:0.324519;171,221,164,255;rgb;cw:0.496394;243,243,61,255;rgb;cw:0.680288;253,174,97,255;rgb;cw:0.832933;230,84,55,255;rgb;ccw"/>
            </Option>
            <prop k="color1" v="17,116,177,255"/>
            <prop k="color2" v="189,37,40,255"/>
            <prop k="direction" v="cw"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="spec" v="rgb"/>
            <prop k="stops" v="0.175481;118,185,169,255;rgb;ccw:0.324519;171,221,164,255;rgb;cw:0.496394;243,243,61,255;rgb;cw:0.680288;253,174,97,255;rgb;cw:0.832933;230,84,55,255;rgb;ccw"/>
          </colorramp>
          <item color="#1174b1" label="-9.911275" value="-9.911274909973145" alpha="255"/>
          <item color="#90cba6" label="-2.532685" value="-2.532684564590454" alpha="255"/>
          <item color="#f3f23e" label="4.845906" value="4.845905780792236" alpha="255"/>
          <item color="#f2854e" label="12.224496" value="12.224496126174927" alpha="255"/>
          <item color="#bd2528" label="19.603086" value="19.603086471557617" alpha="255"/>
          <rampLegendSettings direction="0" useContinuousLegend="1" minimumLabel="" orientation="2" suffix="" prefix="" maximumLabel="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option name="decimal_separator" type="QChar" value=""/>
                <Option name="decimals" type="int" value="6"/>
                <Option name="rounding_type" type="int" value="0"/>
                <Option name="show_plus" type="bool" value="false"/>
                <Option name="show_thousand_separator" type="bool" value="true"/>
                <Option name="show_trailing_zeros" type="bool" value="false"/>
                <Option name="thousand_separator" type="QChar" value=""/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation colorizeOn="0" grayscaleMode="0" colorizeStrength="100" saturation="0" invertColors="0" colorizeGreen="128" colorizeRed="255" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
