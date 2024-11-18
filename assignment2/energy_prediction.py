# وارد کردن کتابخانه‌های مورد نیاز
import pandas as pd  # برای کار با داده‌های جدولی
import numpy as np  # برای انجام عملیات‌های عددی
from sklearn.model_selection import train_test_split  # برای تقسیم داده‌ها به مجموعه‌های آموزشی و تست
from sklearn.preprocessing import StandardScaler  # برای نرمال‌سازی داده‌ها
from sklearn.linear_model import LinearRegression  # مدل رگرسیون خطی
from sklearn.tree import DecisionTreeRegressor  # مدل درخت تصمیم
from sklearn.neural_network import MLPRegressor  # مدل شبکه عصبی (پرسیپترون چندلایه)
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score  # معیارهای ارزیابی مدل
import matplotlib.pyplot as plt  # برای رسم نمودارها

# مرحله 1: جمع‌آوری داده‌ها
print("مرحله 1: جمع‌آوری داده‌ها")

# مشخص کردن مسیر فایل داده‌ها
file_path = 'C:/Users/Mahdi/Desktop/household_power_consumption.txt'

# خواندن داده‌ها از فایل .txt، مشخص کردن جداکننده و نوع داده‌ها
data = pd.read_csv(
    file_path, 
    delimiter=';',  # جداکننده برای داده‌های ورودی
    low_memory=False,  # برای خواندن فایل‌های بزرگ
    na_values='?',  # مقادیر نامعتبر را به NaN تبدیل می‌کند
    dtype={  # تعیین نوع داده‌ها برای هر ستون
        'Global_active_power': 'float64',
        'Global_reactive_power': 'float64',
        'Voltage': 'float64',
        'Global_intensity': 'float64',
        'Sub_metering_1': 'float64',
        'Sub_metering_2': 'float64',
        'Sub_metering_3': 'float64'
    }
)
print("داده‌ها با موفقیت جمع‌آوری شدند")
print(data.head())  # نمایش چند سطر ابتدایی داده‌ها

# مرحله 2: پیش‌پردازش داده‌ها
print("\nمرحله 2: پیش ‌پردازش داده‌ها")

# ترکیب ستون‌های تاریخ و زمان به یک ستون datetime و تنظیم آن به عنوان index
data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d/%m/%Y %H:%M:%S')
data = data.drop(columns=['Date', 'Time'])  # حذف ستون‌های اصلی تاریخ و زمان
data = data.set_index('DateTime')  # تنظیم ستون DateTime به عنوان شاخص


print("اطلاعات مربوط به داده‌ها:")
print(data.info())  # نمایش اطلاعات اولیه داده‌ها

# حذف سطرهایی که داده‌های گمشده دارند
data = data.dropna()

# تقسیم داده‌ها به ویژگی‌ها (X) و هدف (y)
X = data.drop(columns=['Global_active_power'])  # حذف ستون هدف از ویژگی‌ها
y = data['Global_active_power']  # هدف: مصرف انرژی فعال به صورت جهانی

# نرمال‌سازی داده‌ها
scaler = StandardScaler()  # ایجاد شیء استانداردسازی
X = scaler.fit_transform(X)  # اعمال استانداردسازی به داده‌ها
print("پيش پردازش داده ها کامل شد")

# تقسیم داده‌ها به مجموعه‌های آموزشی و تست
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# مرحله 3: ایجاد مدل‌های یادگیری ماشین
print("\nمرحله 3: ایجاد مدل‌های یادگیری ماشین")
# تعریف مدل‌های مختلف
models = {
    'Linear Regression': LinearRegression(),  # مدل رگرسیون خطی
    'Decision Tree': DecisionTreeRegressor(random_state=42),  # مدل درخت تصمیم
    'Neural Network (MLP)': MLPRegressor(hidden_layer_sizes=(100,), max_iter=200, random_state=42)  # مدل شبکه عصبی
}

results = {}  # دیکشنری برای ذخیره نتایج مدل‌ها

for name, model in models.items():
    print(f"\nآموزش مدل: {name}")
    if name == 'Neural Network (MLP)':  # آموزش مدل شبکه عصبی با داده‌های دسته‌بندی شده
        chunk_size = 1000
        print("آموزش مدل شبکه عصبی با استفاده از پردازش داده‌ها در دسته‌های کوچک...")
        for i in range(0, X_train.shape[0], chunk_size):
            X_chunk = X_train[i:i + chunk_size]
            y_chunk = y_train.iloc[i:i + chunk_size].to_numpy()  # تبدیل Series به numpy array
            model.partial_fit(X_chunk, y_chunk.ravel())  # استفاده از ravel() برای تبدیل به آرایه 1D
    else:
        model.fit(X_train, y_train)  # آموزش مدل‌های دیگر

    predictions = model.predict(X_test)  # پیش‌بینی بر اساس داده‌های تست

    
    # محاسبه معیارهای ارزیابی مدل
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    results[name] = {'MSE': mse, 'MAE': mae, 'R2': r2}

    # رسم نمودار برای مقایسه مقادیر واقعی و پیش‌بینی شده
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(y_test)), y_test, label='Real', alpha=0.6)
    plt.plot(range(len(y_test)), predictions, label='Predicted', alpha=0.6)
    plt.title(f'{name} Predictions vs Real Values')
    plt.xlabel('Samples')
    plt.ylabel('Energy Consumption (kWh)')
    plt.legend()
    plt.pause(0.1)

# مرحله 4: آزمایش و ارزیابی مدل
print("\nمرحله 4: آزمایش و ارزیابی مدل")
print("\nنتایج مدل‌ها:")
for name, metrics in results.items():
    print(f'{name} - MSE: {metrics["MSE"]}, MAE: {metrics["MAE"]}, R²: {metrics["R2"]}')

# مرحله 5: نتیجه‌گیری
print("\nمرحله 5: نتیجه‌گیری")
best_model = max(results, key=lambda x: results[x]['R2'])
print(f'بهترین مدل: {best_model}')
