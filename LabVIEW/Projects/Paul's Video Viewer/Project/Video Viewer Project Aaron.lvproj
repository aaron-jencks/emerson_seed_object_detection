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
		<Item Name="Averagers" Type="Folder">
			<Item Name="Averager.lvclass" Type="LVClass" URL="../../Classes/Averager/Averager.lvclass"/>
			<Item Name="Standard Averager.lvclass" Type="LVClass" URL="../../Classes/Standard Averager/Standard Averager.lvclass"/>
			<Item Name="Standard RMS.lvclass" Type="LVClass" URL="../../Classes/Standard RMS/Standard RMS.lvclass"/>
		</Item>
		<Item Name="Data Manipulation" Type="Folder">
			<Item Name="Filter 1D Array.vim" Type="VI" URL="../../Filter 1D Array.vim"/>
			<Item Name="Filter 2D Array.vim" Type="VI" URL="../../Filter 2D Array.vim"/>
			<Item Name="Filter Zeros.vim" Type="VI" URL="../../Filter Zeros.vim"/>
			<Item Name="Flatten Multidimensional Array.vim" Type="VI" URL="../../Flatten Multidimensional Array.vim"/>
			<Item Name="Resize Queue.vim" Type="VI" URL="../../Resize Queue.vim"/>
		</Item>
		<Item Name="Frames" Type="Folder">
			<Item Name="ROIed Video Frame.lvclass" Type="LVClass" URL="../../Classes/ROIed Video Frame/ROIed Video Frame.lvclass"/>
			<Item Name="Video Frame.lvclass" Type="LVClass" URL="../../Classes/Video Frame/Video Frame.lvclass"/>
		</Item>
		<Item Name="Tests" Type="Folder">
			<Item Name="Frame Conversion Test.vi" Type="VI" URL="../../Testbenches/Frame Conversion Test.vi"/>
		</Item>
		<Item Name="build_icon.ico" Type="Document" URL="../../build_icon.ico"/>
		<Item Name="Calculate Playback Position.vi" Type="VI" URL="../../Classes/Main/Calculate Playback Position.vi"/>
		<Item Name="Determine Playable.vi" Type="VI" URL="../../Classes/Main/Determine Playable.vi"/>
		<Item Name="Find Timeout.vi" Type="VI" URL="../../Classes/Main/Find Timeout.vi"/>
		<Item Name="main.vi" Type="VI" URL="../../main.vi"/>
		<Item Name="Status STYP.ctl" Type="VI" URL="../../Classes/Main/Status STYP.ctl"/>
		<Item Name="Video File.lvclass" Type="LVClass" URL="../../Classes/Video File/Video File.lvclass"/>
		<Item Name="Video Processor.lvclass" Type="LVClass" URL="../../Classes/Video Processor/Video Processor.lvclass"/>
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
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="nivision.dll" Type="Document" URL="nivision.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nivissvc.dll" Type="Document" URL="nivissvc.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="Depth Comparator" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{9CC07A05-77DF-4CEA-B8B3-016321E312F0}</Property>
				<Property Name="App_INI_GUID" Type="Str">{5E32FF44-A0CC-4302-97A4-4F776FACBCCF}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
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
				<Property Name="Bld_version.build" Type="Int">2</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">depth_comparator.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/Depth Comparator/depth_comparator.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/Depth Comparator/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/build_icon.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{B43F4956-927C-4C1D-840B-1CC202E378AC}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/main.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">Jet Engineering</Property>
				<Property Name="TgtF_fileDescription" Type="Str">Depth Comparator</Property>
				<Property Name="TgtF_internalName" Type="Str">Depth Comparator</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2019 Jet Engineering</Property>
				<Property Name="TgtF_productName" Type="Str">Depth Comparator</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{0533E339-C4DC-4ACD-9DEF-E63AE773A6DC}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">depth_comparator.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>
