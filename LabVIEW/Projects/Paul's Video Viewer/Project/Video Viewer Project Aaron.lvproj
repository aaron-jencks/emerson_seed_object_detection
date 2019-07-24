<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Data Manipulation" Type="Folder">
			<Item Name="Arrays" Type="Folder">
				<Item Name="Averagers" Type="Folder">
					<Item Name="Averager.lvclass" Type="LVClass" URL="../../Classes/Averager/Averager.lvclass"/>
					<Item Name="Standard Averager.lvclass" Type="LVClass" URL="../../Classes/Standard Averager/Standard Averager.lvclass"/>
					<Item Name="Standard RMS.lvclass" Type="LVClass" URL="../../Classes/Standard RMS/Standard RMS.lvclass"/>
					<Item Name="Roughness Averager.lvclass" Type="LVClass" URL="../../Classes/Roughness Averager/Roughness Averager.lvclass"/>
				</Item>
				<Item Name="Graham Scan" Type="Folder">
					<Item Name="Convex Hull Graham Scan.vi" Type="VI" URL="../../Shared/Graham Scan/Convex Hull Graham Scan.vi"/>
					<Item Name="Graham Scan Point.ctl" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Point.ctl"/>
					<Item Name="Map Points to Origin.vi" Type="VI" URL="../../Shared/Graham Scan/Map Points to Origin.vi"/>
					<Item Name="Graham Scan Origin Point STYP.ctl" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Origin Point STYP.ctl"/>
					<Item Name="Graham Scan Bounding Rectangle STYP.ctl" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Bounding Rectangle STYP.ctl"/>
					<Item Name="Graham Scan Cross Product.vi" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Cross Product.vi"/>
					<Item Name="Graham Scan Point Comparison Less Than.vi" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Point Comparison Less Than.vi"/>
					<Item Name="Convex Hull.vi" Type="VI" URL="../../Shared/Graham Scan/Convex Hull.vi"/>
					<Item Name="Graham Scan 3-point Cross Product.vi" Type="VI" URL="../../Shared/Graham Scan/Graham Scan 3-point Cross Product.vi"/>
					<Item Name="Graham Scan Dot Product.vi" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Dot Product.vi"/>
					<Item Name="UnMap Points From Origin.vi" Type="VI" URL="../../Shared/Graham Scan/UnMap Points From Origin.vi"/>
					<Item Name="Graham Scan Point to Graph Point.vi" Type="VI" URL="../../Shared/Graham Scan/Graham Scan Point to Graph Point.vi"/>
				</Item>
				<Item Name="Heapsort" Type="Folder">
					<Item Name="With Numbers" Type="Folder">
						<Item Name="Numeric Heapsort.vim" Type="VI" URL="../../Shared/Graham Scan/Heapsort/Numeric Heapsort.vim"/>
						<Item Name="Numeric Heapify.vi" Type="VI" URL="../../Shared/Graham Scan/Heapsort/Numeric Heapify.vi"/>
					</Item>
					<Item Name="Heapsort.vi" Type="VI" URL="../../Shared/Graham Scan/Heapsort/Heapsort.vi"/>
					<Item Name="Heapify.vi" Type="VI" URL="../../Shared/Graham Scan/Heapsort/Heapify.vi"/>
				</Item>
				<Item Name="BFS" Type="Folder">
					<Item Name="BFS.vi" Type="VI" URL="../../Shared/BFS/BFS.vi"/>
					<Item Name="BFS Find Neighbors.vi" Type="VI" URL="../../Shared/BFS/BFS Find Neighbors.vi"/>
				</Item>
				<Item Name="Filter 1D Array.vim" Type="VI" URL="../../Filter 1D Array.vim"/>
				<Item Name="Filter 2D Array.vim" Type="VI" URL="../../Filter 2D Array.vim"/>
				<Item Name="Filter Zeros.vim" Type="VI" URL="../../Filter Zeros.vim"/>
				<Item Name="Flatten Multidimensional Array.vim" Type="VI" URL="../../Flatten Multidimensional Array.vim"/>
				<Item Name="Roughness.vi" Type="VI" URL="../../Roughness.vi"/>
				<Item Name="Array Min Max.vim" Type="VI" URL="../../Array Min Max.vim"/>
				<Item Name="Segmented Array Average.vim" Type="VI" URL="../../Segmented Array Average.vim"/>
				<Item Name="Slope Spacing and Counting Roughness.vi" Type="VI" URL="../../Slope Spacing and Counting Roughness.vi"/>
				<Item Name="Swap Array Elements.vim" Type="VI" URL="../../Swap Array Elements.vim"/>
				<Item Name="Sequential Range.vim" Type="VI" URL="../../Sequential Range.vim"/>
				<Item Name="Multi-index 2D Array.vi" Type="VI" URL="../../Multi-index 2D Array.vi"/>
				<Item Name="Split Array.vim" Type="VI" URL="../../Split Array.vim"/>
			</Item>
			<Item Name="Queues" Type="Folder">
				<Item Name="Resize Queue.vim" Type="VI" URL="../../Resize Queue.vim"/>
			</Item>
			<Item Name="Images" Type="Folder">
				<Item Name="Depth Array To Image.vi" Type="VI" URL="../../Depth Array To Image.vi"/>
				<Item Name="RGB Depth To Depth Array.vi" Type="VI" URL="../../RGB Depth To Depth Array.vi"/>
				<Item Name="RGB Depth To Grayscale Depth.vi" Type="VI" URL="../../RGB Depth To Grayscale Depth.vi"/>
				<Item Name="Skeletonized Watershed.vi" Type="VI" URL="../../Skeletonized Watershed.vi"/>
			</Item>
			<Item Name="Integer Division.vim" Type="VI" URL="../../Integer Division.vim"/>
			<Item Name="Replace if less than zero.vim" Type="VI" URL="../../Replace if less than zero.vim"/>
			<Item Name="Unpack Vector Array.vim" Type="VI" URL="../../Unpack Vector Array.vim"/>
			<Item Name="Find Vector Distance.vi" Type="VI" URL="../../Find Vector Distance.vi"/>
		</Item>
		<Item Name="Frames" Type="Folder">
			<Item Name="ROIed Video Frame.lvclass" Type="LVClass" URL="../../Classes/ROIed Video Frame/ROIed Video Frame.lvclass"/>
			<Item Name="Video Frame.lvclass" Type="LVClass" URL="../../Classes/Video Frame/Video Frame.lvclass"/>
		</Item>
		<Item Name="Tests" Type="Folder">
			<Item Name="Frame Conversion Test.vi" Type="VI" URL="../../Testbenches/Frame Conversion Test.vi"/>
			<Item Name="Camera Viewing Test.vi" Type="VI" URL="../../Testbenches/Camera Viewing Test.vi"/>
			<Item Name="Segmented Averager Test.vi" Type="VI" URL="../../Testbenches/Segmented Averager Test.vi"/>
			<Item Name="RGB U32 Color Byte Location Test.vi" Type="VI" URL="../../Testbenches/RGB U32 Color Byte Location Test.vi"/>
			<Item Name="Convex Hull Test.vi" Type="VI" URL="../../Testbenches/Convex Hull Test.vi"/>
			<Item Name="Heapsort Test.vi" Type="VI" URL="../../Testbenches/Heapsort Test.vi"/>
		</Item>
		<Item Name="Realsense Camera" Type="Folder">
			<Item Name="Realsense Cam.lvclass" Type="LVClass" URL="../../Classes/Realsense Cam/Realsense Cam.lvclass"/>
			<Item Name="Realsense Cam File Wrapper.lvclass" Type="LVClass" URL="../../Classes/Realsense Cam Video File Wrapper/Realsense Cam File Wrapper.lvclass"/>
			<Item Name="Video Cam Processor.lvclass" Type="LVClass" URL="../../Classes/Video Cam Processor/Video Cam Processor.lvclass"/>
		</Item>
		<Item Name="build_icon.ico" Type="Document" URL="../../build_icon.ico"/>
		<Item Name="Calculate Playback Position.vi" Type="VI" URL="../../Classes/Main/Calculate Playback Position.vi"/>
		<Item Name="Determine Playable.vi" Type="VI" URL="../../Classes/Main/Determine Playable.vi"/>
		<Item Name="Find Timeout.vi" Type="VI" URL="../../Classes/Main/Find Timeout.vi"/>
		<Item Name="main.vi" Type="VI" URL="../../main.vi"/>
		<Item Name="Video File.lvclass" Type="LVClass" URL="../../Classes/Video File/Video File.lvclass"/>
		<Item Name="Video Processor.lvclass" Type="LVClass" URL="../../Classes/Video Processor/Video Processor.lvclass"/>
		<Item Name="Status STYP.ctl" Type="VI" URL="../../Classes/Main/Status STYP.ctl"/>
		<Item Name="Get Video Processor.vi" Type="VI" URL="../../Get Video Processor.vi"/>
		<Item Name="Compute Convex Hull from points.vi" Type="VI" URL="../../Shared/Compute Convex Hull from points.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="user.lib" Type="Folder">
				<Item Name="JET_QSM - Add State [Array API].vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM - Add State [Array API].vi"/>
				<Item Name="JET_QSM - Add State [String API].vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM - Add State [String API].vi"/>
				<Item Name="JET_QSM - Add State to Front [Array API].vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM - Add State to Front [Array API].vi"/>
				<Item Name="JET_QSM - Add State to Front [String API].vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM - Add State to Front [String API].vi"/>
				<Item Name="JET_QSM - Add State(s).vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Add State(s).vi"/>
				<Item Name="JET_QSM - Add STOP.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Add STOP.vi"/>
				<Item Name="JET_QSM - Flush Debug Queue.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Flush Debug Queue.vi"/>
				<Item Name="JET_QSM - Flush.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Flush.vi"/>
				<Item Name="JET_QSM - Get Next State.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Get Next State.vi"/>
				<Item Name="JET_QSM - Initialize.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Initialize.vi"/>
				<Item Name="JET_QSM - INVALID State.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - INVALID State.vi"/>
				<Item Name="JET_QSM - Set Debug Options.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Public/JET_QSM - Set Debug Options.vi"/>
				<Item Name="JET_QSM_Debug STYP.ctl" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM_Debug STYP.ctl"/>
				<Item Name="JET_QSM_Element STYP.ctl" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM_Element STYP.ctl"/>
				<Item Name="JET_QSM_InvalidOption STYP.ctl" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM_InvalidOption STYP.ctl"/>
				<Item Name="JET_QSM_Refnum STYP.ctl" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET_QSM/Code/Private/JET_QSM_Refnum STYP.ctl"/>
				<Item Name="VI Control - Disable Control.vi" Type="VI" URL="/&lt;userlib&gt;/Jet Engineering/JET VI Control/VI Control - Disable Control.vi"/>
				<Item Name="Ranged Random Number.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Random/Ranged Random Number.vim"/>
				<Item Name="Random Array.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Random/Random Array.vim"/>
				<Item Name="Pythagorean Theorem.vim" Type="VI" URL="/&lt;userlib&gt;/Aaron/Math/Pythagorean Theorem.vim"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Color to RGB.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/Color to RGB.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="General Error Handler Core CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler Core CORE.vi"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="Image Type" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Type"/>
				<Item Name="IMAQ AVI2 Close" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Close"/>
				<Item Name="IMAQ AVI2 Codec Path.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Codec Path.ctl"/>
				<Item Name="IMAQ AVI2 Get Info" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Get Info"/>
				<Item Name="IMAQ AVI2 Open" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Open"/>
				<Item Name="IMAQ AVI2 Read Frame" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Read Frame"/>
				<Item Name="IMAQ AVI2 Refnum.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Avi.llb/IMAQ AVI2 Refnum.ctl"/>
				<Item Name="IMAQ Copy" Type="VI" URL="/&lt;vilib&gt;/vision/Management.llb/IMAQ Copy"/>
				<Item Name="IMAQ Create" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Create"/>
				<Item Name="IMAQ Dispose" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Dispose"/>
				<Item Name="IMAQ Image.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/IMAQ Image.ctl"/>
				<Item Name="IMAQ ImageToArray" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ImageToArray"/>
				<Item Name="IMAQ Overlay ROI" Type="VI" URL="/&lt;vilib&gt;/vision/Overlay.llb/IMAQ Overlay ROI"/>
				<Item Name="Is Path and Not Empty.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Is Path and Not Empty.vi"/>
				<Item Name="Is Value Changed.vim" Type="VI" URL="/&lt;vilib&gt;/Utility/Is Value Changed.vim"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="LVRectTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVRectTypeDef.ctl"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_AALPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALPro.lvlib"/>
				<Item Name="NI_Vision_Development_Module.lvlib" Type="Library" URL="/&lt;vilib&gt;/vision/NI_Vision_Development_Module.lvlib"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="ROI Descriptor" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/ROI Descriptor"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="FixBadRect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pictutil.llb/FixBadRect.vi"/>
				<Item Name="imagedata.ctl" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/imagedata.ctl"/>
				<Item Name="Draw Flattened Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Flattened Pixmap.vi"/>
				<Item Name="Flatten Pixmap.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pixmap.llb/Flatten Pixmap.vi"/>
				<Item Name="ex_CorrectErrorChain.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_CorrectErrorChain.vi"/>
				<Item Name="subFile Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/express/express input/FileDialogBlock.llb/subFile Dialog.vi"/>
				<Item Name="Color (U64)" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Color (U64)"/>
				<Item Name="IMAQ ArrayToColorImage" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ArrayToColorImage"/>
				<Item Name="NI_Gmath.lvlib" Type="Library" URL="/&lt;vilib&gt;/gmath/NI_Gmath.lvlib"/>
				<Item Name="IMAQ ArrayToImage" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ArrayToImage"/>
				<Item Name="IMAQ ColorImageToArray" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ColorImageToArray"/>
				<Item Name="Assert Fractional Numeric Type.vim" Type="VI" URL="/&lt;vilib&gt;/Utility/TypeAssert/Assert Fractional Numeric Type.vim"/>
				<Item Name="Assert Integer Type.vim" Type="VI" URL="/&lt;vilib&gt;/Utility/TypeAssert/Assert Integer Type.vim"/>
				<Item Name="NI_AAL_Geometry.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AAL_Geometry.lvlib"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="nivision.dll" Type="Document" URL="nivision.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nivissvc.dll" Type="Document" URL="nivissvc.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="libRealSense3.lvlib" Type="Library" URL="../../Classes/Realsense Cam/realsense_wrapper_api/libRealSense3.lvlib"/>
			<Item Name="realsense2.dll" Type="Document" URL="../../Classes/Realsense Cam/realsense_wrapper_api/realsense2.dll"/>
			<Item Name="rs3 get stream profile data.vi" Type="VI" URL="../../../../../../../Temp/realsense_labview_sdk/RealSense SDK2.11.0 for LabVIEW/rs3 get stream profile data.vi"/>
			<Item Name="rs3 get stream intrinsics3.vi" Type="VI" URL="../../../../../../../Temp/realsense_labview_sdk/RealSense SDK2.11.0 for LabVIEW/rs3 get stream intrinsics3.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Depth Comparator" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{9CC07A05-77DF-4CEA-B8B3-016321E312F0}</Property>
				<Property Name="App_INI_GUID" Type="Str">{5E32FF44-A0CC-4302-97A4-4F776FACBCCF}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_waitDebugging" Type="Bool">true</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{EFB3F1F3-74E4-4F06-8F65-C602874D873B}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">Depth Comparator</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds/Depth Comparator</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{6242D609-D6AA-4BE1-93A6-56F5C5D0F999}</Property>
				<Property Name="Bld_version.build" Type="Int">7</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">depth_comparator.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/Depth Comparator/depth_comparator.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/Depth Comparator/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/build_icon.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{A9DF8057-7EA9-4C45-811D-9363E3CF947B}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/main.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">Jet Engineering</Property>
				<Property Name="TgtF_enableDebugging" Type="Bool">true</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Depth Comparator</Property>
				<Property Name="TgtF_internalName" Type="Str">Depth Comparator</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2019 Jet Engineering</Property>
				<Property Name="TgtF_productName" Type="Str">Depth Comparator</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{0533E339-C4DC-4ACD-9DEF-E63AE773A6DC}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">depth_comparator.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
			<Item Name="My Installer" Type="Installer">
				<Property Name="Destination[0].name" Type="Str">Depth Video Comparator</Property>
				<Property Name="Destination[0].parent" Type="Str">{3912416A-D2E5-411B-AFEE-B63654D690C0}</Property>
				<Property Name="Destination[0].tag" Type="Str">{F3D4D8A7-C6E3-416D-8A6C-327C04020564}</Property>
				<Property Name="Destination[0].type" Type="Str">userFolder</Property>
				<Property Name="DestinationCount" Type="Int">1</Property>
				<Property Name="DistPart[0].flavorID" Type="Str">DefaultFull</Property>
				<Property Name="DistPart[0].productID" Type="Str">{9D84F59F-9F6D-451C-AF3F-322898F486E2}</Property>
				<Property Name="DistPart[0].productName" Type="Str">NI Vision Common Resources 2018</Property>
				<Property Name="DistPart[0].upgradeCode" Type="Str">{409BEFA9-EB3E-472F-AD77-271A4A1D5927}</Property>
				<Property Name="DistPart[1].flavorID" Type="Str">DefaultFull</Property>
				<Property Name="DistPart[1].productID" Type="Str">{667BCF43-47B8-4CDF-B482-B839AB467FDF}</Property>
				<Property Name="DistPart[1].productName" Type="Str">NI Vision Runtime 2018</Property>
				<Property Name="DistPart[1].upgradeCode" Type="Str">{63DF74E5-A5C9-11D4-814E-005004D6CDD6}</Property>
				<Property Name="DistPart[2].flavorID" Type="Str">DefaultFull</Property>
				<Property Name="DistPart[2].productID" Type="Str">{8B546CAB-5BE1-4E80-AB65-A47E8E8B0BC0}</Property>
				<Property Name="DistPart[2].productName" Type="Str">NI LabVIEW Runtime 2018 f2 (64-bit)</Property>
				<Property Name="DistPart[2].SoftDep[0].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[0].productName" Type="Str">NI ActiveX Container (64-bit)</Property>
				<Property Name="DistPart[2].SoftDep[0].upgradeCode" Type="Str">{1038A887-23E1-4289-B0BD-0C4B83C6BA21}</Property>
				<Property Name="DistPart[2].SoftDep[1].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[1].productName" Type="Str">Math Kernel Libraries 2017</Property>
				<Property Name="DistPart[2].SoftDep[1].upgradeCode" Type="Str">{699C1AC5-2CF2-4745-9674-B19536EBA8A3}</Property>
				<Property Name="DistPart[2].SoftDep[10].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[10].productName" Type="Str">NI Deployment Framework 2018</Property>
				<Property Name="DistPart[2].SoftDep[10].upgradeCode" Type="Str">{838942E4-B73C-492E-81A3-AA1E291FD0DC}</Property>
				<Property Name="DistPart[2].SoftDep[11].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[11].productName" Type="Str">NI Error Reporting 2018 (64-bit)</Property>
				<Property Name="DistPart[2].SoftDep[11].upgradeCode" Type="Str">{785BE224-E5B2-46A5-ADCB-55C949B5C9C7}</Property>
				<Property Name="DistPart[2].SoftDep[2].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[2].productName" Type="Str">Math Kernel Libraries 2018</Property>
				<Property Name="DistPart[2].SoftDep[2].upgradeCode" Type="Str">{33A780B9-8BDE-4A3A-9672-24778EFBEFC4}</Property>
				<Property Name="DistPart[2].SoftDep[3].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[3].productName" Type="Str">NI Logos 18.0</Property>
				<Property Name="DistPart[2].SoftDep[3].upgradeCode" Type="Str">{5E4A4CE3-4D06-11D4-8B22-006008C16337}</Property>
				<Property Name="DistPart[2].SoftDep[4].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[4].productName" Type="Str">NI TDM Streaming 18.0</Property>
				<Property Name="DistPart[2].SoftDep[4].upgradeCode" Type="Str">{4CD11BE6-6BB7-4082-8A27-C13771BC309B}</Property>
				<Property Name="DistPart[2].SoftDep[5].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[5].productName" Type="Str">NI LabVIEW Web Server 2018 (64-bit)</Property>
				<Property Name="DistPart[2].SoftDep[5].upgradeCode" Type="Str">{5F449D4C-83B9-492E-986B-6B85A29C431D}</Property>
				<Property Name="DistPart[2].SoftDep[6].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[6].productName" Type="Str">NI LabVIEW Real-Time NBFifo 2018</Property>
				<Property Name="DistPart[2].SoftDep[6].upgradeCode" Type="Str">{EF4708F6-5A34-4DBA-B12B-79CC2004E20B}</Property>
				<Property Name="DistPart[2].SoftDep[7].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[7].productName" Type="Str">NI VC2010MSMs</Property>
				<Property Name="DistPart[2].SoftDep[7].upgradeCode" Type="Str">{EFBA6F9E-F934-4BD7-AC51-60CCA480489C}</Property>
				<Property Name="DistPart[2].SoftDep[8].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[8].productName" Type="Str">NI VC2015 Runtime</Property>
				<Property Name="DistPart[2].SoftDep[8].upgradeCode" Type="Str">{D42E7BAE-6589-4570-B6A3-3E28889392E7}</Property>
				<Property Name="DistPart[2].SoftDep[9].exclude" Type="Bool">false</Property>
				<Property Name="DistPart[2].SoftDep[9].productName" Type="Str">NI mDNS Responder 17.0</Property>
				<Property Name="DistPart[2].SoftDep[9].upgradeCode" Type="Str">{9607874B-4BB3-42CB-B450-A2F5EF60BA3B}</Property>
				<Property Name="DistPart[2].SoftDepCount" Type="Int">12</Property>
				<Property Name="DistPart[2].upgradeCode" Type="Str">{E4F03E30-E086-4EFC-B703-16299EC18DC7}</Property>
				<Property Name="DistPartCount" Type="Int">3</Property>
				<Property Name="INST_author" Type="Str">Jet Engineering</Property>
				<Property Name="INST_autoIncrement" Type="Bool">true</Property>
				<Property Name="INST_buildLocation" Type="Path">../builds/Depth Video Comparator/My Installer</Property>
				<Property Name="INST_buildLocation.type" Type="Str">relativeToCommon</Property>
				<Property Name="INST_buildSpecName" Type="Str">My Installer</Property>
				<Property Name="INST_defaultDir" Type="Str">{F3D4D8A7-C6E3-416D-8A6C-327C04020564}</Property>
				<Property Name="INST_productName" Type="Str">Depth Video Comparator</Property>
				<Property Name="INST_productVersion" Type="Str">1.0.1</Property>
				<Property Name="InstSpecBitness" Type="Str">64-bit</Property>
				<Property Name="InstSpecVersion" Type="Str">18008012</Property>
				<Property Name="MSI_arpCompany" Type="Str">Jet Engineering</Property>
				<Property Name="MSI_autoselectDrivers" Type="Bool">true</Property>
				<Property Name="MSI_distID" Type="Str">{C0F339D1-413E-4BA4-A830-98410EE1A49A}</Property>
				<Property Name="MSI_hideNonRuntimes" Type="Bool">true</Property>
				<Property Name="MSI_osCheck" Type="Int">0</Property>
				<Property Name="MSI_upgradeCode" Type="Str">{3AD1C742-DD85-4622-AD36-20DC4E8692E5}</Property>
				<Property Name="RegDest[0].dirName" Type="Str">Software</Property>
				<Property Name="RegDest[0].dirTag" Type="Str">{DDFAFC8B-E728-4AC8-96DE-B920EBB97A86}</Property>
				<Property Name="RegDest[0].parentTag" Type="Str">2</Property>
				<Property Name="RegDestCount" Type="Int">1</Property>
				<Property Name="Source[0].dest" Type="Str">{F3D4D8A7-C6E3-416D-8A6C-327C04020564}</Property>
				<Property Name="Source[0].File[0].dest" Type="Str">{F3D4D8A7-C6E3-416D-8A6C-327C04020564}</Property>
				<Property Name="Source[0].File[0].name" Type="Str">depth_comparator.exe</Property>
				<Property Name="Source[0].File[0].Shortcut[0].destIndex" Type="Int">0</Property>
				<Property Name="Source[0].File[0].Shortcut[0].name" Type="Str">depth_comparator</Property>
				<Property Name="Source[0].File[0].Shortcut[0].subDir" Type="Str">Video Viewer Project Aaron</Property>
				<Property Name="Source[0].File[0].ShortcutCount" Type="Int">1</Property>
				<Property Name="Source[0].File[0].tag" Type="Str">{0533E339-C4DC-4ACD-9DEF-E63AE773A6DC}</Property>
				<Property Name="Source[0].FileCount" Type="Int">1</Property>
				<Property Name="Source[0].name" Type="Str">Depth Comparator</Property>
				<Property Name="Source[0].tag" Type="Ref">/My Computer/Build Specifications/Depth Comparator</Property>
				<Property Name="Source[0].type" Type="Str">EXE</Property>
				<Property Name="SourceCount" Type="Int">1</Property>
			</Item>
		</Item>
	</Item>
</Project>
