<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Classes" Type="Folder">
			<Item Name="Video Processor" Type="Folder" URL="/&lt;userlib&gt;/Aaron/File IO/Video/Video Processor">
				<Property Name="NI.DISK" Type="Bool">true</Property>
			</Item>
			<Item Name="EdgeDetectionProcessor.lvclass" Type="LVClass" URL="../../Classes/EdgeDetectionProcessor/EdgeDetectionProcessor.lvclass"/>
		</Item>
		<Item Name="Easy Derivative.vim" Type="VI" URL="../../Data Manipulation/Easy Derivative.vim"/>
		<Item Name="Find Curvature.vim" Type="VI" URL="../../Data Manipulation/Find Curvature.vim"/>
		<Item Name="main.vi" Type="VI" URL="../../main.vi"/>
		<Item Name="Pythagorean Theorem.vim" Type="VI" URL="../../Data Manipulation/Pythagorean Theorem.vim"/>
		<Item Name="Vector Magnitude.vim" Type="VI" URL="../../Data Manipulation/Vector Magnitude.vim"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="user.lib" Type="Folder">
				<Item Name="Averager.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Arrays/Averagers/Averager/Averager.lvclass"/>
				<Item Name="Clone Image to New Image.vi" Type="VI" URL="/&lt;userlib&gt;/Aaron/Image Manipulation/Clone Image to New Image.vi"/>
				<Item Name="Filter 1D Array.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Arrays/Filter 1D Array.vim"/>
				<Item Name="Filter Zeros.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Arrays/Filter Zeros.vim"/>
				<Item Name="Flatten Multidimensional Array.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Arrays/Flatten Multidimensional Array.vim"/>
				<Item Name="Pop First and Last.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Arrays/Pop First and Last.vim"/>
				<Item Name="Resize Queue.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Queues/Resize Queue.vim"/>
				<Item Name="ROIed Video Frame.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/Aaron/File IO/Video/Frames/ROIed Video Frame/ROIed Video Frame.lvclass"/>
				<Item Name="Standard Averager.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/Aaron/Data Manipulation/Arrays/Averagers/Standard Averager/Standard Averager.lvclass"/>
				<Item Name="Video File.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/Aaron/File IO/Video/Video File/Video File.lvclass"/>
				<Item Name="Video Frame.lvclass" Type="LVClass" URL="/&lt;userlib&gt;/Aaron/File IO/Video/Frames/Video Frame/Video Frame.lvclass"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Color to RGB.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/Color to RGB.vi"/>
				<Item Name="Image Type" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Type"/>
				<Item Name="Image Unit" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Unit"/>
				<Item Name="IMAQ AVI2 Close" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Close"/>
				<Item Name="IMAQ AVI2 Codec Path.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Codec Path.ctl"/>
				<Item Name="IMAQ AVI2 Get Info" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Get Info"/>
				<Item Name="IMAQ AVI2 Open" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Open"/>
				<Item Name="IMAQ AVI2 Read Frame" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Read Frame"/>
				<Item Name="IMAQ AVI2 Refnum.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Refnum.ctl"/>
				<Item Name="IMAQ Convert from Curves Internal" Type="VI" URL="/&lt;vilib&gt;/vision/Analysis.llb/IMAQ Convert from Curves Internal"/>
				<Item Name="IMAQ Convert To Curve Parameters Internal" Type="VI" URL="/&lt;vilib&gt;/vision/Pattern Matching.llb/IMAQ Convert To Curve Parameters Internal"/>
				<Item Name="IMAQ Copy" Type="VI" URL="/&lt;vilib&gt;/vision/Management.llb/IMAQ Copy"/>
				<Item Name="IMAQ Create" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Create"/>
				<Item Name="IMAQ Curve Parameters Internal.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Pattern Matching.llb/IMAQ Curve Parameters Internal.ctl"/>
				<Item Name="IMAQ Curve Parameters.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Pattern Matching.llb/IMAQ Curve Parameters.ctl"/>
				<Item Name="IMAQ Dispose" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Dispose"/>
				<Item Name="IMAQ ExtractCurvesCurve.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Analysis.llb/IMAQ ExtractCurvesCurve.ctl"/>
				<Item Name="IMAQ ExtractCurvesCurveInternal.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Analysis.llb/IMAQ ExtractCurvesCurveInternal.ctl"/>
				<Item Name="IMAQ GetImageInfo" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ GetImageInfo"/>
				<Item Name="IMAQ GetImageSize" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ GetImageSize"/>
				<Item Name="IMAQ Image.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/IMAQ Image.ctl"/>
				<Item Name="IMAQ ImageToArray" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ImageToArray"/>
				<Item Name="IMAQ Overlay Points" Type="VI" URL="/&lt;vilib&gt;/vision/Overlay.llb/IMAQ Overlay Points"/>
				<Item Name="IMAQ Overlay ROI" Type="VI" URL="/&lt;vilib&gt;/vision/Overlay.llb/IMAQ Overlay ROI"/>
				<Item Name="IMAQ SetImageSize" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ SetImageSize"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_AALPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALPro.lvlib"/>
				<Item Name="NI_Vision_Development_Module.lvlib" Type="Library" URL="/&lt;vilib&gt;/vision/NI_Vision_Development_Module.lvlib"/>
				<Item Name="ROI Descriptor" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/ROI Descriptor"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="nivision.dll" Type="Document" URL="nivision.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nivissvc.dll" Type="Document" URL="nivissvc.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
