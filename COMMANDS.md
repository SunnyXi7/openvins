# OpenVINS 閉環測試指令

## 📋 完整測試流程（三個指令）

### 1️⃣ 啟動 RealSense D455 相機

```bash
ros2 launch realsense2_camera rs_launch.py enable_gyro:=true enable_accel:=true unite_imu_method:=2 enable_sync:=true enable_infra1:=true enable_infra2:=true
```

### 2️⃣ 啟動 OpenVINS + RViz2（在新終端）

```bash
ros2 launch ov_msckf subscribe.launch.py \
  config:=rs_d455_stereo \
  max_cameras:=2 \
  use_stereo:=true \
  rviz_enable:=true \
  topic_imu:=/camera/camera/imu \
  topic_camera0:=/camera/camera/infra1/image_rect_raw \
  topic_camera1:=/camera/camera/infra2/image_rect_raw \
  topic_camera0_info:=/camera/camera/infra1/camera_info \
  filepath_est:=/tmp/ov_estimate.txt \
  filepath_std:=/tmp/ov_estimate_std.txt \
  save_total_state:=true
```

**測試步驟**:
1. 等待系統初始化完成
2. 從起點出發，走一個閉環路徑
3. 回到起點後，按 `Ctrl+C` 停止 OpenVINS

### 3️⃣ 誤差評估

測試完成後執行：

```bash
python3 /home/sunny/openvins_ws/analyze_results.py /tmp/ov_estimate.txt
```

**輸出結果**:
- ✅ 起始點到終點的誤差 (Start-to-End Error)
- ✅ 總路徑長度 (Path Length)
- ✅ 漂移百分比 (Drift Percentage)
- ✅ XY 平面軌跡圖 (保存為 `/tmp/ov_estimate_plot.png`)

---

## 📊 評估指標說明

- **Start-to-End Error (Drift)**: 閉環測試中起點和終點的距離誤差（單位：米）
- **Drift Percentage**: 漂移百分比 = (起終點誤差 / 總路徑長度) × 100%
- **良好表現**: 漂移百分比 < 1% 表示系統表現優秀

---

## �️ 查看軌跡圖

```bash
eog /tmp/ov_estimate_plot.png
```

或複製到工作目錄保存：

```bash
cp /tmp/ov_estimate.txt ~/openvins_ws/closed_loop_$(date +%Y%m%d_%H%M%S).txt
cp /tmp/ov_estimate_plot.png ~/openvins_ws/closed_loop_$(date +%Y%m%d_%H%M%S).png
```

---

## 🔧 注意事項

1. **記得先 source 環境**：在新終端執行前，先運行：
   ```bash
   cd /home/sunny/openvins_ws
   source install/setup.bash
   ```

2. **評估程式碼位置**：`analyze_results.py` 應該在 openvins_ws 根目錄

3. **結果文件位置**：軌跡數據保存在 `/tmp/` 目錄，重啟後會消失，記得及時備份
