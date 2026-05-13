from supabase import create_client, Client
import os

class SupabaseAPI:
    """
    Sebuah kelas untuk menyederhanakan operasi CRUD dan kueri dengan Supabase.
    """
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Menginisialisasi klien SupabaseAPI.

        Args:
            supabase_url (str): URL proyek Supabase Anda.
            supabase_key (str): Kunci API publik (kunci anon) proyek Supabase Anda.
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)

    def sign_up(self, email: str, password: str):
        """
        Mendaftarkan pengguna baru dengan email dan kata sandi.

        Args:
            email (str): Alamat email pengguna.
            password (str): Kata sandi pengguna.

        Returns:
            User: Objek pengguna yang dibuat jika berhasil, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> user = api.sign_up("test@example.com", "password123")
            >>> if user:
            ...     print(f"Pengguna {user.email} berhasil mendaftar.")
        """
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            return response.user
        except Exception as e:
            print(f"Error signing up: {e}")
            return None

    def sign_in(self, email: str, password: str):
        """
        Masuk sebagai pengguna yang sudah ada dengan email dan kata sandi.

        Args:
            email (str): Alamat email pengguna.
            password (str): Kata sandi pengguna.

        Returns:
            User: Objek pengguna yang masuk jika berhasil, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> user = api.sign_in("test@example.com", "password123")
            >>> if user:
            ...     print(f"Pengguna {user.email} berhasil masuk.")
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response.user
        except Exception as e:
            print(f"Error signing in: {e}")
            return None

    def sign_out(self):
        """
        Keluar dari pengguna saat ini.

        Returns:
            bool: True jika keluar berhasil, False jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> if api.sign_out():
            ...     print("Pengguna berhasil keluar.")
        """
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception as e:
            print(f"Error signing out: {e}")
            return False

    def create_data(self, table_name: str, data: dict):
        """
        Memasukkan data baru ke dalam tabel yang ditentukan.

        Args:
            table_name (str): Nama tabel.
            data (dict): Kamus yang berisi data untuk dimasukkan.

        Returns:
            list: Daftar objek data yang dimasukkan jika berhasil, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> new_item = {"name": "Item A", "price": 10.99}
            >>> created_data = api.create_data("products", new_item)
            >>> if created_data:
            ...     print(f"Data yang dibuat: {created_data}")
        """
        try:
            response = self.supabase.table(table_name).insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error creating data: {e}")
            return None

    def read_data(self, table_name: str, query_params: dict = None):
        """
        Membaca data dari tabel yang ditentukan, dengan parameter kueri opsional.

        Args:
            table_name (str): Nama tabel.
            query_params (dict, optional): Kamus pasangan kunci-nilai untuk memfilter hasil. Defaultnya None.

        Returns:
            list: Daftar objek data jika berhasil, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> all_products = api.read_data("products")
            >>> if all_products:
            ...     print(f"Semua produk: {all_products}")
            >>> filtered_products = api.read_data("products", {"price": 10.99})
            >>> if filtered_products:
            ...     print(f"Produk yang difilter: {filtered_products}")
        """
        try:
            query = self.supabase.table(table_name).select("*")
            if query_params:
                for key, value in query_params.items():
                    query = query.eq(key, value)
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error reading data: {e}")
            return None

    def update_data(self, table_name: str, query_column: str, query_value: str, data: dict):
        """
        Memperbarui data dalam tabel yang ditentukan berdasarkan kueri.

        Args:
            table_name (str): Nama tabel.
            query_column (str): Kolom yang digunakan untuk memfilter pembaruan.
            query_value (str): Nilai yang cocok di query_column.
            data (dict): Kamus yang berisi data untuk diperbarui.

        Returns:
            list: Daftar objek data yang diperbarui jika berhasil, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> updated_item = {"price": 12.50}
            >>> updated_data = api.update_data("products", "name", "Item A", updated_item)
            >>> if updated_data:
            ...     print(f"Data yang diperbarui: {updated_data}")
        """
        try:
            response = self.supabase.table(table_name).update(data).eq(query_column, query_value).execute()
            return response.data
        except Exception as e:
            print(f"Error updating data: {e}")
            return None

    def delete_data(self, table_name: str, query_column: str, query_value: str):
        """
        Menghapus data dari tabel yang ditentukan berdasarkan kueri.

        Args:
            table_name (str): Nama tabel.
            query_column (str): Kolom yang digunakan untuk memfilter penghapusan.
            query_value (str): Nilai yang cocok di query_column.

        Returns:
            list: Daftar objek data yang dihapus jika berhasil, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> deleted_data = api.delete_data("products", "name", "Item A")
            >>> if deleted_data:
            ...     print(f"Data yang dihapus: {deleted_data}")
        """
        try:
            response = self.supabase.table(table_name).delete().eq(query_column, query_value).execute()
            return response.data
        except Exception as e:
            print(f"Error deleting data: {e}")
            return None

    def get_user_by_email(self, table_name: str, email: str):
        """
        Mengambil pengguna dari tabel yang ditentukan berdasarkan alamat email mereka.

        Args:
            table_name (str): Nama tabel tempat data pengguna disimpan.
            email (str): Alamat email pengguna yang akan diambil.

        Returns:
            dict: Objek pengguna jika ditemukan, None jika tidak.

        Example:
            >>> api = SupabaseAPI("URL_SUPABASE_ANDA", "KUNCI_SUPABASE_ANDA")
            >>> user = api.get_user_by_email("users", "test@example.com")
            >>> if user:
            ...     print(f"Pengguna ditemukan: {user}")
        """
        try:
            response = self.supabase.table(table_name).select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def readFilterColumn(self, table_name:str, column:str, value:str) :
        try:
            response = self.supabase.table(table_name).select("*") \
                .eq(column,value) \
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None    
