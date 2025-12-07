print("Nhập các dòng văn bản (nhấn Enter hai lần để kết thúc):")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
print("\nCác dòng đã nhập sau khi chuyển thanh chữ in hoa:")
for line in lines:
    print(line.upper())
