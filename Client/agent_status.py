import psycopg2
from datetime import datetime, timedelta, timezone
import argparse
from colorama import Fore, Style, init
import sys
# Khởi tạo colorama
init(autoreset=True)

# Hàm kết nối đến PostgreSQL
def connect_db():
    return psycopg2.connect("postgres://avnadmin:AVNS_-KEo1AvB98NH557DB5v@pg-18c83e66-d-nips.d.aivencloud.com:20242/mydb?sslmode=require")

# Lấy danh sách agent từ DB
def fetch_agents(cursor, minutes=None, show_all=False):
    if show_all:
        cursor.execute('SELECT "ID", "LAST_SEEN" FROM public."AGENTS"')
    else:
        time_threshold = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        cursor.execute("""
            SELECT "ID", "LAST_SEEN"
            FROM public."AGENTS"
            WHERE "LAST_SEEN" > %s
        """, (time_threshold,))
    return cursor.fetchall()

def main():
    parser = argparse.ArgumentParser(description="Kiểm tra trạng thái các agent.")
    parser.add_argument("--minutes", type=int, default=5, help="Thời gian tính hoạt động (phút)")
    parser.add_argument("--all", action="store_true", help="Hiển thị tất cả agent, kể cả đã offline")
    args = parser.parse_args()


    if len(sys.argv) == 1:
        # print("ℹ️  Không có tham số nào được truyền. Hiển thị hướng dẫn sử dụng:\n")
        # parser = argparse.ArgumentParser(description="🔍 Kiểm tra trạng thái các agent.")
        parser.print_help()
        sys.exit(0)

    try:
        conn = connect_db()
        cursor = conn.cursor()

        agents = fetch_agents(cursor, args.minutes, args.all)

        # print(f"\n🕒 Kiểm tra trạng thái agent {'(TẤT CẢ)' if args.all else f'trong {args.minutes} phút gần đây'}...\n")

        if not agents:
            print("⚠️  Không có agent nào được tìm thấy.")
        else:
            now = datetime.now(timezone.utc)
            for agent_id, last_seen in agents:
                delta = now - last_seen
                if delta <= timedelta(minutes=args.minutes):
                    status = f"{Fore.GREEN}🟢 ONLINE"
                else:
                    status = f"{Fore.RED}🔴 OFFLINE"
                print(f"{status}{Style.RESET_ALL} | ID: {agent_id} | Last seen: {last_seen.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
