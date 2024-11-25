import pandas as pd  # برای پردازش داده‌ها به صورت ساختاریافته
import numpy as np  # برای عملیات عددی و کار با آرایه‌ها
import tensorflow as tf  # برای طراحی و اجرای مدل‌های یادگیری عمیق
from sklearn.preprocessing import StandardScaler  # برای نرمال‌سازی داده‌ها
from sklearn.model_selection import train_test_split  # برای تقسیم داده‌ها به مجموعه‌های آموزش و آزمایش
from sklearn.metrics import classification_report, accuracy_score  # برای ارزیابی مدل
import matplotlib.pyplot as plt  # برای رسم نمودارها
import dask.dataframe as dd  # برای پردازش موازی داده‌های بزرگ

# مرحله 1: جمع‌آوری داده‌ها
print("مرحله 1: جمع‌آوری داده‌ها")

# مسیر فایل داده‌ها (فایل ورودی شامل داده‌های شبکه برای شناسایی نفوذ)
file_path = 'C:/Users/Mahdi/Desktop/KDDCup99.txt'

# بارگذاری داده‌ها با استفاده از Dask برای پردازش موازی (پردازش سریع‌تر داده‌های بزرگ)
data = dd.read_csv(file_path, delimiter=',', na_values='?', assume_missing=True)

# استخراج 10000 ردیف اول داده‌ها برای کاهش حجم پردازش
data = data.head(10000)

# نمایش پیام موفقیت در جمع‌آوری داده‌ها
print("داده‌ها با موفقیت جمع‌آوری شدند")

# نمایش چند ردیف اول داده‌ها برای بررسی
print(data.head())

# مرحله 2: پیش‌پردازش داده‌ها
print("\nمرحله 2: پیش‌پردازش داده‌ها")

# تعریف نقشه‌برداری برای تبدیل برچسب‌های متنی (labels) به مقادیر عددی
label_mapping = {
    'normal': 0,  # رفتار عادی
    'buffer_overflow': 1, 'loadmodule': 1, 'perl': 1, 'neptune': 1, 'smurf': 1,
    'guess_passwd': 1, 'pod': 1, 'teardrop': 1, 'portsweep': 1, 'ipsweep': 1,
    'land': 1, 'ftp_write': 1, 'back': 1, 'imap': 1, 'satan': 1, 'phf': 1,
    'nmap': 1, 'multihop': 1, 'warezmaster': 1, 'warezclient': 1, 'spy': 1,
    'rootkit': 1  # رفتارهای غیرعادی (حملات)
}

# اعمال نقشه‌برداری به ستون برچسب‌ها
data['label'] = data['label'].map(label_mapping)

# حذف ردیف‌هایی که برچسب آنها مقدار Null دارد
data = data.dropna(subset=['label'])

# تبدیل ویژگی‌های متنی به کدهای عددی (برای استفاده در مدل یادگیری ماشین)
data['protocol_type'] = data['protocol_type'].astype('category').cat.codes
data['service'] = data['service'].astype('category').cat.codes
data['flag'] = data['flag'].astype('category').cat.codes

# جدا کردن ویژگی‌ها (X) و برچسب‌ها (y)
X = data.drop(columns=['label'])  # حذف ستون برچسب‌ها برای استفاده به‌عنوان ویژگی
y = data['label']  # برچسب‌ها (هدف)

# نرمال‌سازی داده‌های ویژگی‌ها برای بهبود عملکرد مدل
scaler = StandardScaler()
X = scaler.fit_transform(X)

# تقسیم داده‌ها به مجموعه‌های آموزش (80%) و آزمایش (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# بررسی عدم وجود مقادیر NaN در برچسب‌های آموزشی و آزمایشی
assert not np.any(np.isnan(y_train)), "y_train contains NaN values"
assert not np.any(np.isnan(y_test)), "y_test contains NaN values"

# تغییر شکل داده‌ها به 3 بعد برای ورودی مدل RNN
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))  # تغییر شکل داده‌های آموزشی
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))  # تغییر شکل داده‌های آزمایشی

# مرحله 3: طراحی مدل
print("\nمرحله 3: طراحی مدل")

# تعریف مدل RNN با استفاده از LSTM
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1], X_train.shape[2])),  # لایه ورودی با شکل داده
    tf.keras.layers.LSTM(64, return_sequences=False),  # لایه LSTM با 64 واحد
    tf.keras.layers.Dense(32, activation='relu'),  # لایه Dense با 32 نرون و فعال‌سازی ReLU
    tf.keras.layers.Dense(1, activation='sigmoid')  # لایه خروجی با فعال‌سازی سیگموئید (برای طبقه‌بندی دودویی)
])

# کامپایل مدل با تابع هزینه و بهینه‌ساز
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# تعریف Early Stopping برای جلوگیری از آموزش بیش از حد (Overfitting)
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# تعریف Learning Rate Scheduler برای کاهش تدریجی نرخ یادگیری در هر epoch
lr_scheduler = tf.keras.callbacks.LearningRateScheduler(
    lambda epoch: 1e-3 * 0.7 ** epoch, verbose=True)

# مرحله 4: آموزش مدل
print("\nمرحله 4: آموزش مدل")

# آموزش مدل با داده‌های آموزشی و اعتبارسنجی بر اساس داده‌های آزمایشی
history = model.fit(X_train, y_train, epochs=20, batch_size=128, validation_data=(X_test, y_test),
                    callbacks=[early_stopping, lr_scheduler])

# مرحله 5: ارزیابی مدل
print("\nمرحله 5: ارزیابی مدل")

# پیش‌بینی بر روی داده‌های آزمایشی
y_pred = (model.predict(X_test) > 0.5).astype("int32")  # تبدیل احتمال به مقادیر 0 یا 1

# تولید و نمایش گزارش طبقه‌بندی (شامل دقت، یادآوری، و F1-Score)
print(classification_report(y_test, y_pred))

# محاسبه و نمایش دقت مدل
accuracy = accuracy_score(y_test, y_pred)
print(f"دقت مدل: {accuracy * 100:.2f}%")

# مرحله 6: تحلیل نتایج
print("\nمرحله 6: تحلیل نتایج")

# رسم نمودار دقت در طول epoch‌ها برای آموزش و اعتبارسنجی
plt.figure(figsize=(10, 6))  # تنظیم ابعاد نمودار
plt.plot(history.history['accuracy'], label='Training Accuracy')  # نمودار دقت آموزشی
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')  # نمودار دقت اعتبارسنجی
plt.title('Model Accuracy Over Epochs')  # عنوان نمودار
plt.xlabel('Epochs')  # برچسب محور افقی
plt.ylabel('Accuracy')  # برچسب محور عمودی
plt.legend()  # افزودن راهنما به نمودار
plt.show()  # نمایش نمودار
