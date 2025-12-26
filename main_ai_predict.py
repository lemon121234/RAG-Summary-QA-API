"""
AI 預測模型主入口
展示分層架構設計
"""
import numpy as np
from ai_predict import Predictor, DataPreprocessor, FeatureExtractor


def main():
    """主函數 - 完整的預測流程示例"""
    print("=" * 60)
    print("🤖 AI 預測模型 - 分層架構示例")
    print("=" * 60)
    
    # 1. 生成示例數據
    print("\n📊 步驟 1: 準備數據")
    np.random.seed(42)
    n_samples = 100
    n_features = 3
    
    # 生成特徵數據（模擬真實場景）
    X_raw = np.random.randn(n_samples, n_features) * 10 + 50
    # 生成目標值（線性關係 + 噪音）
    y = (X_raw[:, 0] * 2 + X_raw[:, 1] * 1.5 + X_raw[:, 2] * 0.5 + 
         np.random.randn(n_samples) * 5)
    
    print(f"原始數據形狀: X={X_raw.shape}, y={y.shape}")
    
    # 2. 數據預處理
    print("\n🔧 步驟 2: 數據預處理")
    preprocessor = DataPreprocessor(normalize=True)
    X_processed = preprocessor.fit_transform(X_raw)
    print(f"處理後數據形狀: {X_processed.shape}")
    print(f"標準化統計: mean={preprocessor.mean[:2]}, std={preprocessor.std[:2]}")
    
    # 3. 特徵提取
    print("\n🎯 步驟 3: 特徵提取")
    feature_extractor = FeatureExtractor()
    
    # 提取基本特徵
    basic_features = feature_extractor.extract_basic_features(X_processed)
    print(f"基本特徵數量: {len(basic_features)}")
    
    # 提取時間序列特徵（如果適用）
    temporal_features = feature_extractor.extract_temporal_features(
        X_processed.flatten()[:20], window_size=3
    )
    print(f"時間序列特徵數量: {len(temporal_features)}")
    
    # 組合特徵
    combined_features = feature_extractor.combine_features(
        basic_features, temporal_features
    )
    print(f"組合後特徵數量: {len(combined_features)}")
    
    # 4. 分割訓練集和測試集
    print("\n📦 步驟 4: 數據分割")
    split_idx = int(n_samples * 0.8)
    X_train, X_test = X_processed[:split_idx], X_processed[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    print(f"訓練集: {X_train.shape[0]} 樣本")
    print(f"測試集: {X_test.shape[0]} 樣本")
    
    # 5. 訓練模型
    print("\n🚀 步驟 5: 訓練模型")
    predictor = Predictor(model_type='random_forest')
    train_metrics = predictor.train(X_train, y_train)
    print(f"訓練指標: MSE={train_metrics['train_mse']:.2f}, "
          f"MAE={train_metrics['train_mae']:.2f}, "
          f"R²={train_metrics['train_r2']:.3f}")
    
    # 6. 模型評估
    print("\n📈 步驟 6: 模型評估")
    test_metrics = predictor.evaluate(X_test, y_test)
    print(f"測試指標:")
    print(f"  - MSE (均方誤差): {test_metrics['mse']:.2f}")
    print(f"  - MAE (平均絕對誤差): {test_metrics['mae']:.2f}")
    print(f"  - RMSE (均方根誤差): {test_metrics['rmse']:.2f}")
    print(f"  - R² (決定係數): {test_metrics['r2']:.3f}")
    
    # 7. 特徵重要性
    print("\n🔍 步驟 7: 特徵重要性分析")
    feature_importance = predictor.get_feature_importance()
    if feature_importance is not None:
        print(f"特徵重要性: {feature_importance}")
        print(f"最重要特徵索引: {np.argmax(feature_importance)}")
    
    # 8. 進行預測
    print("\n🎯 步驟 8: 進行預測")
    sample_X = X_test[:5]
    predictions = predictor.predict(sample_X)
    actual = y_test[:5]
    
    print("預測結果對比:")
    for i, (pred, actual_val) in enumerate(zip(predictions, actual)):
        error = abs(pred - actual_val)
        print(f"  樣本 {i+1}: 預測={pred:.2f}, 實際={actual_val:.2f}, "
              f"誤差={error:.2f}")


if __name__ == "__main__":
    main()

