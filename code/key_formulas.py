"""
КЛЮЧЕВЫЕ ФОРМУЛЫ ФИНАНСОВОЙ МОДЕЛИ ОБНАРУЖЕНИЯ ПУЗЫРЕЙ
=====================================================
Этот файл содержит ключевые математические формулы и алгоритмы, 
используемые в системе обнаружения финансовых пузырей.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression

# ========================================================================
# I. ПРОИЗВОДНЫЕ МЕТРИКИ И ИНДИКАТОРЫ (из data_preparation.py)
# ========================================================================

def key_derived_metrics(df):
    """
    Примеры из модуля data_preparation.py:
    Ключевые формулы расчета производных метрик
    """
    
    # 1. Расчет соотношения VIX к S&P 500 (индикатор страха/жадности)
    df['VIX_SPX_ratio'] = df['VIX'] / df['SPX'] * 100
    
    # 2. Расчет дивидендной доходности
    df['Dividend_Yield'] = (df['Dividend_D'] / df['SPX']) * 100
    
    # 3. Логарифмическая доходность (для расчета волатильности)
    df['SPX_log_return'] = np.log(df['SPX'] / df['SPX'].shift(1))
    
    # 4. Расчет волатильности на различных временных горизонтах
    # (21 день ~ 1 месяц, 63 дня ~ 3 месяца, 252 дня ~ 1 год)
    for window in [21, 63, 252]:
        df[f'SPX_volatility_{window}d'] = df['SPX_log_return'].rolling(window=window).std() * np.sqrt(252)
    
    return df


# ========================================================================
# II. ОПРЕДЕЛЕНИЕ ЭКСПОНЕНЦИАЛЬНОГО РОСТА (из data_preparation.py)
# ========================================================================

def exponential_growth_metrics(df):
    """
    Определение и измерение экспоненциального роста цен
    """
    
    # 1. Годовое изменение цены S&P 500
    df['SPX_growth_rate'] = df['SPX'].pct_change(periods=12)
    
    # 2. Расчет экспоненциального тренда на 5-летнем скользящем окне
    # Используем линейную регрессию на логарифмированных данных
    # Коэффициент наклона * 12 * 100 = годовой % роста в экспоненциальном тренде
    df['SPX_exp_trend'] = df['SPX'].rolling(window=60).apply(
        lambda x: np.polyfit(np.arange(len(x)), np.log(x), 1)[0] * 12 * 100,
        raw=True
    )
    
    # 3. Отклонение фактического роста от экспоненциального тренда
    # Положительное значение = рост быстрее тренда (потенциальный пузырь)
    df['SPX_exp_deviation'] = df['SPX_growth_rate'] - df['SPX_exp_trend']
    
    return df


def check_exponential_growth(price_series):
    """
    Проверка наличия экспоненциального роста в ценовом ряде
    
    Возвращает:
    - exp_score: метрику экспоненциальности (произведение наклона и R²)
    - is_exponential: булево значение о наличии экспоненциального роста
    """
    # Логарифмируем данные для проверки на экспоненциальность
    log_values = np.log(price_series)
    x = np.arange(len(price_series))
    
    # Линейная регрессия на логарифмированных данных
    # Если рост экспоненциальный, то логарифмированный ряд будет линейным
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, log_values)
    
    # Метрика экспоненциальности: произведение наклона и коэффициента детерминации
    # Высокое значение = крутой наклон с хорошим качеством подгонки (R²)
    exp_score = slope * r_value**2 * 100
    
    # Определяем наличие экспоненциального роста на основе порога
    is_exponential = exp_score > 2.0 and r_value**2 > 0.9
    
    return exp_score, is_exponential


# ========================================================================
# III. РАСЧЕТ Z-SCORE И ПРОЦЕНТИЛЬНЫХ РАНГОВ (из data_preparation.py и bubble_metrics.py)
# ========================================================================

def calculate_zscore(df, metric, window=60):
    """
    Расчет Z-score для метрики (отклонение от среднего в единицах стандартного отклонения)
    """
    # Скользящее среднее за 5 лет (60 месяцев)
    rolling_mean = df[metric].rolling(window=window).mean()
    
    # Скользящее стандартное отклонение за 5 лет
    rolling_std = df[metric].rolling(window=window).std()
    
    # Расчет Z-score: (значение - среднее) / стандартное отклонение
    z_score = (df[metric] - rolling_mean) / rolling_std
    
    return z_score


def calculate_percentile_rank(df, metric, window=120, invert=False):
    """
    Расчет процентильного ранга метрики относительно исторического распределения
    
    Параметры:
    - metric: метрика для расчета ранга
    - window: размер окна для расчета ранга
    - invert: инвертировать ранг (для метрик, где низкие значения = высокий риск)
    """
    # Расчет процентильного ранга на расширяющемся окне
    # (каждое значение сравнивается со всеми предыдущими значениями)
    pct_rank = df[metric].expanding(min_periods=window).apply(
        lambda x: stats.percentileofscore(x, x.iloc[-1]) / 100
    )
    
    # Инвертируем ранг, если необходимо
    # (для метрик, где низкие значения означают высокий риск)
    if invert:
        pct_rank = 1 - pct_rank
        
    return pct_rank


# ========================================================================
# IV. РАСЧЕТ КАТЕГОРИАЛЬНЫХ РИСКОВ (из bubble_metrics.py)
# ========================================================================

def calculate_category_risk(df, metrics, direction_dict=None):
    """
    Расчет категориального риска на основе нескольких метрик
    
    Параметры:
    - metrics: список метрик для включения в расчет категориального риска
    - direction_dict: словарь с направлениями метрик (1: высокие значения = риск, -1: низкие значения = риск)
    """
    if direction_dict is None:
        direction_dict = {metric: 1 for metric in metrics}
    
    # Список метрик с добавленным суффиксом _pct_rank
    rank_metrics = [f"{metric}_pct_rank" for metric in metrics if f"{metric}_pct_rank" in df.columns]
    
    if not rank_metrics:
        return pd.Series(np.nan, index=df.index)
        
    # Среднее значение процентильных рангов для метрик в категории
    category_risk = df[rank_metrics].mean(axis=1)
    
    return category_risk


# ========================================================================
# V. РАСЧЕТ КОМПОЗИТНОГО ИНДЕКСА ПУЗЫРЯ (из bubble_metrics.py)
# ========================================================================

def calculate_composite_bubble_score(df, category_scores, weights):
    """
    Расчет композитного индекса пузыря на основе взвешенного среднего категориальных рисков
    
    Параметры:
    - category_scores: список столбцов с категориальными оценками риска
    - weights: список весов для каждой категории
    """
    # Нормализация весов (сумма = 1)
    weights = np.array(weights) / sum(weights)
    
    # Взвешенная сумма категориальных рисков
    composite_score = np.zeros(len(df))
    for i, category in enumerate(category_scores):
        if category in df.columns:
            composite_score += df[category].values * weights[i]
    
    # Сглаженная версия (3-месячное скользящее среднее)
    composite_score_smooth = pd.Series(composite_score, index=df.index).rolling(window=3).mean()
    
    # Определение уровня риска на основе композитного индекса
    risk_levels = pd.cut(
        composite_score,
        bins=[-float('inf'), 0.3, 0.5, 0.7, float('inf')],
        labels=['Low', 'Medium', 'High', 'Critical']
    )
    
    # Расчет моментума (изменение первого порядка)
    momentum = pd.Series(composite_score, index=df.index).diff().rolling(window=3).mean()
    
    # Расчет ускорения (изменение второго порядка)
    acceleration = momentum.diff().rolling(window=3).mean()
    
    return pd.DataFrame({
        'composite_bubble_score': composite_score,
        'composite_bubble_score_smooth': composite_score_smooth,
        'bubble_risk_level': risk_levels,
        'bubble_score_momentum': momentum,
        'bubble_score_acceleration': acceleration
    }, index=df.index)


# ========================================================================
# VI. СИСТЕМА РАННЕГО ПРЕДУПРЕЖДЕНИЯ (из bubble_metrics.py)
# ========================================================================

def calculate_early_warning_signals(df, metrics, warning_threshold=0.7, danger_threshold=0.9):
    """
    Расчет сигналов раннего предупреждения на основе пороговых значений
    """
    warning_columns = []
    danger_columns = []
    
    # Генерация предупреждений и опасностей для каждой метрики
    for metric in metrics:
        rank_col = f"{metric}_pct_rank"
        if rank_col not in df.columns:
            continue
            
        # Создание бинарных индикаторов предупреждения и опасности
        warning_col = f"{metric}_warning"
        danger_col = f"{metric}_danger"
        
        df[warning_col] = (df[rank_col] > warning_threshold) * 1
        df[danger_col] = (df[rank_col] > danger_threshold) * 1
        
        warning_columns.append(warning_col)
        danger_columns.append(danger_col)
    
    # Подсчет общего количества предупреждений и опасностей
    df['total_warnings'] = df[warning_columns].sum(axis=1)
    df['total_dangers'] = df[danger_columns].sum(axis=1)
    
    # Максимальное возможное количество предупреждений и опасностей
    max_warnings = len(warning_columns)
    max_dangers = len(danger_columns)
    
    # Сигнал ускорения пузыря (положительное ускорение при высоком композитном индексе)
    if 'bubble_score_acceleration' in df.columns and 'composite_bubble_score' in df.columns:
        df['acceleration_signal'] = (
            (df['bubble_score_acceleration'] > 0) & 
            (df['composite_bubble_score'] > 0.5)
        )
    
    # Сигнал потенциального разворота (отрицательное ускорение при очень высоком композитном индексе)
    if 'bubble_score_acceleration' in df.columns and 'composite_bubble_score' in df.columns:
        df['reversal_signal'] = (
            (df['bubble_score_acceleration'] < 0) & 
            (df['composite_bubble_score'] > 0.7)
        )
    
    # Композитный индекс раннего предупреждения 
    # (взвешенная сумма доли предупреждений и опасностей)
    df['early_warning_index'] = (
        (df['total_warnings'] / max_warnings) * 0.4 + 
        (df['total_dangers'] / max_dangers) * 0.6
    )
    
    # Категоризация уровня предупреждения
    df['warning_level'] = pd.cut(
        df['early_warning_index'],
        bins=[-float('inf'), 0.3, 0.6, 0.8, float('inf')],
        labels=['Normal', 'Watch', 'Warning', 'Alert']
    )
    
    return df


# ========================================================================
# VII. ФУНКЦИИ ПРОГНОЗИРОВАНИЯ (из bubble_forecast.py)
# ========================================================================

def prepare_time_series_features(series, lookback=12):
    """
    Подготовка временного ряда для прогнозирования путем создания признаков
    
    Параметры:
    - series: временной ряд для прогнозирования
    - lookback: количество исторических периодов для расчета признаков
    """
    df = pd.DataFrame(index=series.index)
    
    # 1. Лаги (предыдущие значения)
    for lag in [1, 3, 6, 12]:
        df[f'lag_{lag}'] = series.shift(lag)
    
    # 2. Скользящие средние
    for window in [3, 6, 12]:
        df[f'ma_{window}'] = series.rolling(window=window).mean()
    
    # 3. Темпы изменения
    for window in [1, 3, 6]:
        df[f'pct_change_{window}'] = series.pct_change(periods=window)
    
    # 4. Расчет тренда на основе линейной регрессии на предыдущих значениях
    df['trend'] = np.nan
    for i in range(lookback, len(series) + 1):
        y_segment = series.iloc[i-lookback:i].values
        X = np.arange(lookback).reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y_segment)
        df.loc[df.index[i-1], 'trend'] = model.coef_[0]
    
    # 5. Сезонность (разница с аналогичным периодом прошлого года)
    df['seasonal'] = series - series.shift(12)
    
    # 6. Волатильность
    df['volatility'] = series.rolling(window=lookback).std()
    
    # Добавляем целевую переменную
    df['target'] = series
    
    return df.dropna()


def forecast_bubble_metrics(df, forecast_horizon=24, metrics=None):
    """
    Прогнозирование ключевых метрик и индекса пузыря
    
    Параметры:
    - df: исходный датафрейм с данными
    - forecast_horizon: горизонт прогнозирования в месяцах
    - metrics: список метрик для прогнозирования (если None, используются стандартные метрики)
    """
    if metrics is None:
        metrics = [
            'SPX', 'VIX', 'The_Buffett_Indicator', 'CAPE_or_Earnings_Ratio_P_E10',
            'PE_Ratio', 'Dividend_Yield', 'BAA10YM', 'Fed_funds_rate', 
            'GDP_growth', 'Inflation', 'Unemployment', 'Yield_spread',
            'composite_bubble_score'
        ]
    
    # Создание датафрейма для хранения прогнозов
    last_date = df.index[-1]
    future_dates = pd.date_range(start=last_date, periods=forecast_horizon+1, freq='MS')[1:]
    forecasts = pd.DataFrame(index=future_dates)
    
    # Прогнозирование каждой метрики отдельно
    for metric in metrics:
        if metric not in df.columns:
            continue
            
        # Подготовка признаков для обучения
        features_df = prepare_time_series_features(df[metric])
        
        # Разделение на признаки и целевую переменную
        X = features_df.drop('target', axis=1)
        y = features_df['target']
        
        # Обучение модели случайного леса
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Пошаговое прогнозирование на будущие периоды
        current_df = df.copy()
        future_values = []
        
        for _ in range(forecast_horizon):
            # Подготовка признаков для последней точки
            last_features = prepare_time_series_features(current_df[metric]).iloc[-1:].drop('target', axis=1)
            
            # Прогноз следующего значения
            next_value = model.predict(last_features)[0]
            future_values.append(next_value)
            
            # Добавление прогноза в текущий датафрейм
            next_idx = current_df.index[-1] + pd.DateOffset(months=1)
            next_row = pd.DataFrame({metric: next_value}, index=[next_idx])
            current_df = pd.concat([current_df, next_row])
        
        # Добавление прогноза в итоговый датафрейм
        forecasts[metric] = future_values
    
    # Расчет изменений для каждой метрики (относительно последнего известного значения)
    for metric in forecasts.columns:
        last_value = df[metric].iloc[-1]
        forecasts[f'{metric}_Change'] = (forecasts[metric] - last_value) / last_value * 100
    
    # Если прогнозируется композитный индекс пузыря, добавляем категоризацию риска
    if 'composite_bubble_score' in forecasts.columns:
        forecasts['bubble_risk_level'] = pd.cut(
            forecasts['composite_bubble_score'],
            bins=[-float('inf'), 0.3, 0.5, 0.7, float('inf')],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
    
    return forecasts


# ========================================================================
# VIII. ОПРЕДЕЛЕНИЕ РЫНОЧНЫХ РЕЖИМОВ (из bubble_metrics.py)
# ========================================================================

def detect_market_regimes(df, n_clusters=4):
    """
    Определение рыночных режимов с помощью алгоритма кластеризации
    
    Параметры:
    - df: датафрейм с данными
    - n_clusters: количество режимов/кластеров для определения
    """
    # Выбор метрик для определения режимов
    regime_features = [
        'SPX_volatility_21d', 'SPX_growth_rate', 
        'VIX_SPX_ratio', 'BAA10YM', 
        'composite_bubble_score'
    ]
    
    available_features = [f for f in regime_features if f in df.columns]
    
    if len(available_features) < 2:
        return pd.Series(np.nan, index=df.index)
    
    # Подготовка данных для кластеризации
    X = df[available_features].dropna()
    
    # Если недостаточно данных, возвращаем NaN
    if len(X) < n_clusters * 2:
        return pd.Series(np.nan, index=df.index)
    
    # Нормализация данных для кластеризации
    X_scaled = (X - X.mean()) / X.std()
    
    # Применение алгоритма K-means для определения кластеров/режимов
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Создание серии с режимами
    market_regimes = pd.Series(np.nan, index=df.index)
    market_regimes.loc[X.index] = clusters
    
    # Определение описательных имен для режимов на основе их характеристик
    regime_profiles = {}
    
    for cluster in range(n_clusters):
        cluster_data = X[market_regimes == cluster]
        
        # Профиль кластера (средние значения для каждой метрики)
        profile = cluster_data.mean()
        
        # Определение характеристик режима на основе профиля
        volatility = profile.get('SPX_volatility_21d', np.nan)
        growth = profile.get('SPX_growth_rate', np.nan)
        bubble_score = profile.get('composite_bubble_score', np.nan)
        
        # Простая классификация режима
        if pd.isna(volatility) or pd.isna(growth) or pd.isna(bubble_score):
            regime_name = f"Regime {cluster+1}"
        elif volatility > 0.5 and growth < 0:
            regime_name = "Crisis"
        elif volatility > 0.3 and bubble_score > 0.7:
            regime_name = "Bubble"
        elif bubble_score > 0.6:
            regime_name = "Overheating"
        elif growth > 0.1:
            regime_name = "Bull Market"
        elif growth < -0.1:
            regime_name = "Bear Market"
        elif volatility < 0.2 and abs(growth) < 0.05:
            regime_name = "Stagnation"
        else:
            regime_name = "Normal"
            
        regime_profiles[cluster] = regime_name
    
    # Создание серии с названиями режимов
    market_regime_names = market_regimes.copy()
    for cluster, name in regime_profiles.items():
        market_regime_names.loc[market_regimes == cluster] = name
    
    return market_regime_names
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans