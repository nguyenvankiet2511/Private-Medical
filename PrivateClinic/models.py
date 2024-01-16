from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, DATE, Text, Enum, Time
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
from PrivateClinic import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    EMPLOYEE = 4
    PATIENT = 5


class Nguoi(db.Model):
    __tablename__ = 'nguoi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    ngaySinh = Column(DATE, nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    diaChi = Column(String(100), nullable=False)
    soDienThoai = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    # Các mối quan hệ
    taiKhoan = relationship('TaiKhoan', backref='Nguoi', lazy=True)
    bacsi = relationship('BacSi', backref='Nguoi', uselist=False)
    yta = relationship('YTa', backref='Nguoi', uselist=False)
    benhnhan = relationship('BenhNhan', backref='Nguoi', uselist=False)
    nhanvien = relationship('NhanVien', backref='Nguoi', uselist=False)
    quantri = relationship('QuanTriVien', backref='Nguoi', uselist=False)


class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'tai_khoan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    trangThai = Column(Boolean, nullable=True)
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    # Các mối quan hệ
    id_nguoidung = Column(Integer, ForeignKey(Nguoi.id), nullable=False, unique=True)


class BenhNhan(db.Model):
    __tablename__ = 'benh_nhan'
    id = Column(Integer, ForeignKey(Nguoi.id), primary_key=True, unique=True)
    phieu_kham = relationship('PhieuKham', backref='benh_nhan', uselist=False)
    ct_ds_kham = relationship('ChiTietDanhSach', backref='benh_nhan', lazy=True)
    ds_dk = relationship('DanhSachDangKy', backref='benh_nhan', lazy=True)


class DanhSachDangKy(db.Model):
    __tablename__ = 'danh_sach_dang_ky'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayDK = Column(DATE, default=datetime.now())
    ngayHen = Column(DATE, nullable=False)
    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id))


class DanhSachKham(db.Model):
    __tablename__ = 'danh_sach_kham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(DATE, nullable=False)
    chi_tiet_ds = relationship('ChiTietDanhSach', backref='danh_sach_kham', lazy=True)


class YTa(db.Model):
    __tablename__ = 'y_ta'
    id = Column(Integer, ForeignKey(Nguoi.id), primary_key=True)
    bangCap = Column(String(150), nullable=False)


class BacSi(db.Model):
    __tablename__ = 'bac_si'
    id = Column(Integer, ForeignKey(Nguoi.id), primary_key=True)
    chungChi = Column(String(150), nullable=False)
    chuyenKhoa = Column(String(150), nullable=True)
    ct_ds = relationship('ChiTietDanhSach', backref='bac_si', lazy=True)


class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'
    id = Column(Integer, ForeignKey(Nguoi.id), primary_key=True, unique=True)
    bangCap = Column(String(150), nullable=False)


class QuanTriVien(db.Model):
    __tablename__ = 'quan_tri'
    id = Column(Integer, ForeignKey(Nguoi.id), primary_key=True, unique=True)


class ChiTietDanhSach(db.Model):
    __tablename__ = 'ct_danh_sach'
    id = Column(Integer, primary_key=True, autoincrement=True)
    danhSachKham_id = Column(Integer, ForeignKey(DanhSachKham.id))
    is_active = Column(Boolean, default=True)
    benhNhan_id = Column(Integer, ForeignKey(BenhNhan.id))
    bacSi_id = Column(Integer, ForeignKey(BacSi.id))


class PhieuKham(db.Model):
    __tablename__ = 'phieu_kham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chuanDoan = Column(String(250), nullable=False)
    ngayKham = Column(DATE, nullable=False)
    trieuChung = Column(String(250), nullable=False)
    # Các mối quan hệ
    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id))
    hoa_don = relationship('HoaDon', backref='phieu_kham', lazy=True)
    phieu_thuoc = relationship('PhieuThuoc', backref="phieu_kham", lazy=True)


class HoaDon(db.Model):  # hóa đơn
    __tablename__ = 'hoa_don'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(DATE, nullable=False)
    tienKham = Column(Float, nullable=False)
    tienThuoc = Column(Float, nullable=False)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id))


class DonViThuoc(db.Model):  # đơn vị thuốc
    __tablename__ = 'don_vi_thuoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenDonVi = Column(String(50), nullable=False)
    moTa = Column(String(300), nullable=False)
    thuoc = relationship('Thuoc', backref='don_vi_thuoc', lazy=True)

    def __str__(self):
        return self.tenDonVi


class DanhMuc(db.Model):
    __tablename__ = 'danh_muc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenDanhMuc = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='danh_muc', lazy=True)

    def __str__(self):
        return self.tenDanhMuc


class Thuoc(db.Model):  # thuốc
    __tablename__ = 'thuoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    moTa = Column(String(300), nullable=False)
    gia = Column(Float, default=0)
    trangThai = Column(Boolean, nullable=False)
    don_vi_thuoc_id = Column(Integer, ForeignKey(DonViThuoc.id))
    danh_muc_id = Column(Integer, ForeignKey(DanhMuc.id))
    phieu_thuoc = relationship('PhieuThuoc', backref='thuoc', lazy=True)

    def __str__(self):
        return self.tenThuoc


class PhieuThuoc(db.Model):
    __tablename__ = 'phieu_thuoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    soLuong = Column(Integer, nullable=False)
    cachDung = Column(String(300), nullable=False)
    #
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id), nullable=False)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)


class QuyDinh(db.Model):
    __tablename__ = 'quy_dinh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenQD = Column(String(100), nullable=False)
    giaTri = Column(Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        ds_quydinh = [
            QuyDinh(tenQD='Tiền khám', giaTri=100000),
            QuyDinh(tenQD='Sô lượng thuốc', giaTri=30),
            QuyDinh(tenQD='Số lượng đơn vị', giaTri=3),
            QuyDinh(tenQD='Số lượng bệnh khám trong ngày', giaTri=40)
        ]
        db.session.add_all(ds_quydinh)
        db.session.commit()
        # dữ liệu bảng Nguoi, 30 dòng-----------------------------------------------------------------------
        ds_nguoi = [
            Nguoi(hoTen="Nguyễn Văn An", ngaySinh=date(2000, 1, 10), gioiTinh=True,
                  diaChi="123 Đường Lê Lợi, Quận 1, TP.Hồ Chí Minh", soDienThoai='0123456789',
                  email='nguyen.van.an@gmail.com'),
            Nguoi(hoTen="Trần Thị Bảo", ngaySinh=date(1995, 5, 20), gioiTinh=False,
                  diaChi="456 Đường Nguyễn Huệ, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
                  email='tran.thi.bao@gmail.com'),
            Nguoi(hoTen="Phạm Văn Cường", ngaySinh=date(1988, 8, 5), gioiTinh=True,
                  diaChi="789 Đường Võ Văn Tần, Quận 10, TP.Hồ Chí Minh", soDienThoai='0123987654',
                  email='pham.van.cuong@gmail.com'),
            Nguoi(hoTen="Lê Minh Dương", ngaySinh=date(2002, 2, 15), gioiTinh=True,
                  diaChi="101 Đường Phan Chu Trinh, Quận 5, TP.Hồ Chí Minh", soDienThoai='0345678901',
                  email='le.minh.duong@gmail.com'),
            Nguoi(hoTen="Hoàng Thị Em", ngaySinh=date(1990, 10, 25), gioiTinh=False,
                  diaChi="202 Đường Bùi Viện, Quận 1, TP.Hồ Chí Minh", soDienThoai='0765432109',
                  email='hoang.thi.em@gmail.com'),
            Nguoi(hoTen="Ngô Văn Phúc", ngaySinh=date(1985, 3, 8), gioiTinh=True,
                  diaChi="303 Đường Lý Tự Trọng, Quận 3, TP.Hồ Chí Minh", soDienThoai='0912345678',
                  email='ngo.van.phuc@gmail.com'),
            Nguoi(hoTen="Vũ Thị Hoa", ngaySinh=date(1998, 7, 17), gioiTinh=False,
                  diaChi="404 Đường Trần Hưng Đạo, Quận 1, TP.Hồ Chí Minh", soDienThoai='0654321098',
                  email='vu.thi.hoa@gmail.com'),
            Nguoi(hoTen="Đinh Văn Giang", ngaySinh=date(1993, 4, 30), gioiTinh=True,
                  diaChi="505 Đường Cách Mạng Tháng Tám, Quận 3, TP.Hồ Chí Minh", soDienThoai='0123456789',
                  email='dinh.van.giang@gmail.com'),
            Nguoi(hoTen="Bùi Thị Hồng", ngaySinh=date(1996, 6, 11), gioiTinh=False,
                  diaChi="606 Đường Võ Thị Sáu, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
                  email='bui.thi.hong@gmail.com'),
            Nguoi(hoTen="Lý Văn Anh", ngaySinh=date(1991, 9, 3), gioiTinh=True,
                  diaChi="707 Đường Nguyễn Đình Chính, Quận Phú Nhuận, TP.Hồ Chí Minh", soDienThoai='0123987654',
                  email='ly.van.anh@gmail.com'),
            Nguoi(hoTen="Mai Thị Kim", ngaySinh=date(1989, 11, 22), gioiTinh=False,
                  diaChi="808 Đường Huỳnh Khương Ninh, Quận 1, TP.Hồ Chí Minh", soDienThoai='0345678901',
                  email='mai.thi.kim@gmail.com'),
            Nguoi(hoTen="Hồ Văn Long", ngaySinh=date(2001, 12, 7), gioiTinh=True,
                  diaChi="909 Đường Thống Nhất, Quận Gò Vấp, TP.Hồ Chí Minh", soDienThoai='0765432109',
                  email='ho.van.long@gmail.com'),
            Nguoi(hoTen="Trương Thị Mỹ", ngaySinh=date(1986, 2, 19), gioiTinh=False,
                  diaChi="1010 Đường Hồ Bieu Chanh, Quận 10, TP.Hồ Chí Minh", soDienThoai='0912345678',
                  email='truong.thi.my@gmail.com'),
            Nguoi(hoTen="Đặng Văn Nam", ngaySinh=date(1997, 5, 29), gioiTinh=True,
                  diaChi="1111 Đường Văn Cao, Quận Bình Thạnh, TP.Hồ Chí Minh", soDienThoai='0654321098',
                  email='dang.van.nam@gmail.com'),
            Nguoi(hoTen="Lưu Thị Phương", ngaySinh=date(1994, 8, 14), gioiTinh=False,
                  diaChi="1212 Đường Nguyễn Công Trứ, Quận 4, TP.Hồ Chí Minh", soDienThoai='0123456789',
                  email='luu.thi.phuong@gmail.com'),
            Nguoi(hoTen="Nguyễn Thị Bình", ngaySinh=date(2000, 6, 15), gioiTinh=False,
                  diaChi="456 Đường Hai Bà Trưng, Quận 1, TP.Hồ Chí Minh", soDienThoai='0123456789',
                  email='nguyen.thi.binh@gmail.com'),
            Nguoi(hoTen="Trần Văn Cường", ngaySinh=date(1995, 10, 20), gioiTinh=True,
                  diaChi="789 Đường Lê Duẩn, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
                  email='tran.van.cuong@gmail.com'),
            Nguoi(hoTen="Phạm Thị Diệu", ngaySinh=date(1988, 12, 5), gioiTinh=False,
                  diaChi="101 Đường Nguyễn Thị Minh Khai, Quận 10, TP.Hồ Chí Minh", soDienThoai='0123987654',
                  email='pham.thi.dieu@gmail.com'),
            Nguoi(hoTen="Lê Văn Đức", ngaySinh=date(2002, 3, 25), gioiTinh=True,
                  diaChi="202 Đường Cách Mạng Tháng Tám, Quận 5, TP.Hồ Chí Minh", soDienThoai='0345678901',
                  email='le.van.duc@gmail.com'),
            Nguoi(hoTen="Hoàng Thị Hà", ngaySinh=date(1990, 11, 5), gioiTinh=False,
                  diaChi="303 Đường Trần Hưng Đạo, Quận 1, TP.Hồ Chí Minh", soDienThoai='0765432109',
                  email='hoang.thi.ha@gmail.com'),
            Nguoi(hoTen="Ngô Văn Hải", ngaySinh=date(1985, 7, 8), gioiTinh=True,
                  diaChi="404 Đường Đinh Công Tráng, Quận 3, TP.Hồ Chí Minh", soDienThoai='0912345678',
                  email='ngo.van.hai@gmail.com'),
            Nguoi(hoTen="Vũ Thị Lan", ngaySinh=date(1998, 4, 17), gioiTinh=False,
                  diaChi="505 Đường Huỳnh Khương Ninh, Quận 1, TP.Hồ Chí Minh", soDienThoai='0654321098',
                  email='vu.thi.lan@gmail.com'),
            Nguoi(hoTen="Đinh Văn Khánh", ngaySinh=date(1993, 2, 28), gioiTinh=True,
                  diaChi="606 Đường Cao Thắng, Quận 3, TP.Hồ Chí Minh", soDienThoai='0123456789',
                  email='dinh.van.khanh@gmail.com'),
            Nguoi(hoTen="Bùi Thị Lan Anh", ngaySinh=date(1996, 6, 11), gioiTinh=False,
                  diaChi="707 Đường Võ Thị Sáu, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
                  email='bui.thi.lan.anh@gmail.com'),
            Nguoi(hoTen="Lý Thị Mai", ngaySinh=date(1991, 9, 13), gioiTinh=True,
                  diaChi="808 Đường Bùi Viện, Quận 1, TP.Hồ Chí Minh", soDienThoai='0123987654',
                  email='ly.thi.mai@gmail.com'),
            Nguoi(hoTen="Mai Thị Ngọc", ngaySinh=date(1989, 11, 22), gioiTinh=False,
                  diaChi="909 Đường Lê Thánh Tôn, Quận Gò Vấp, TP.Hồ Chí Minh", soDienThoai='0345678901',
                  email='mai.thi.ngoc@gmail.com'),
            Nguoi(hoTen="Hồ Văn Phú", ngaySinh=date(2001, 12, 7), gioiTinh=True,
                  diaChi="1010 Đường Nguyễn Đình Chính, Quận Phú Nhuận, TP.Hồ Chí Minh", soDienThoai='0765432109',
                  email='ho.van.phu@gmail.com'),
            Nguoi(hoTen="Trương Thị Quỳnh", ngaySinh=date(1986, 2, 19), gioiTinh=False,
                  diaChi="1111 Đường Lê Văn Sỹ, Quận Tân Bình, TP.Hồ Chí Minh", soDienThoai='0912345678',
                  email='truong.thi.quynh@gmail.com'),
            Nguoi(hoTen="Đặng Văn Sơn", ngaySinh=date(1997, 5, 29), gioiTinh=True,
                  diaChi="1212 Đường Điện Biên Phủ, Quận Bình Thạnh, TP.Hồ Chí Minh", soDienThoai='0654321098',
                  email='dang.van.son@gmail.com'),
            Nguoi(hoTen="Lưu Thị Thảo", ngaySinh=date(1994, 8, 14), gioiTinh=False,
                  diaChi="1313 Đường Võ Văn Kiệt, Quận 4, TP.Hồ Chí Minh", soDienThoai='0123456789',
                  email='luu.thi.thao@gmail.com')
        ]
        db.session.add_all(ds_nguoi)
        db.session.commit()
        import hashlib

        ds_tk = [
            TaiKhoan(ten='Admin', username='admin', user_role=UserRole.ADMIN,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=28),
            TaiKhoan(ten='User1', username='bacsi1', user_role=UserRole.DOCTOR,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=13),
            TaiKhoan(ten='User2', username='bacsi2', user_role=UserRole.DOCTOR,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=14),
            TaiKhoan(ten='Moderator1', username='nhanvien1', user_role=UserRole.EMPLOYEE,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=26),
            TaiKhoan(ten='Moderator2', username='yta1', user_role=UserRole.NURSE,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=20),
            TaiKhoan(ten='Guest1', username='yta2', user_role=UserRole.NURSE,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=21),
            TaiKhoan(ten='Guest2', username='nhanvien2', user_role=UserRole.EMPLOYEE,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=25),
            TaiKhoan(ten='Editor1', username='benhnhan1', user_role=UserRole.PATIENT,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=8),
            TaiKhoan(ten='Editor2', username='benhnhan2', user_role=UserRole.PATIENT,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=9),
            TaiKhoan(ten='SuperAdmin', username='benhnhan3', user_role=UserRole.PATIENT,
                     password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), trangThai=True,
                     id_nguoidung=10),
        ]

        db.session.add_all(ds_tk)
        db.session.commit()
        # dữ liệu bệnh nhân, 12 dòng---------------------------------------------------------------------------
        ds_benhnhan = [
            BenhNhan(id=1),
            BenhNhan(id=2),
            BenhNhan(id=3),
            BenhNhan(id=4),
            BenhNhan(id=5),
            BenhNhan(id=6),
            BenhNhan(id=7),
            BenhNhan(id=8),
            BenhNhan(id=9),
            BenhNhan(id=10),
            BenhNhan(id=11),
            BenhNhan(id=12),
        ]
        db.session.add_all(ds_benhnhan)
        db.session.commit()
        # # dữ liệu bác sĩ , 7 dòng-------------------------------------------------------------------
        ds_bacsi = [
            BacSi(id=13, chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Tim Mạch'),
            BacSi(id=14, chungChi='Bác Sĩ Y Học Thực Hành', chuyenKhoa='Cơ Xương Khớp'),
            BacSi(id=15, chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Thần Kinh'),
            BacSi(id=16, chungChi='Bác Sĩ Y Học Thực Hành', chuyenKhoa='Da Liễu'),
            BacSi(id=17, chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Nội Tiêu Hóa'),
            BacSi(id=18, chungChi='Bác Sĩ Y Học Thực Hành', chuyenKhoa='Mắt Học'),
            BacSi(id=19, chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Hô Hấp'),
        ]
        db.session.add_all(ds_bacsi)
        db.session.commit()
        # y tá------------------------------------------------------------------------------
        ds_yta = [
            YTa(id=20, bangCap='Đại học'),
            YTa(id=21, bangCap='Thạc sĩ'),
            YTa(id=22, bangCap='Đại học'),
            YTa(id=23, bangCap='Thạc sĩ'),
            YTa(id=24, bangCap='Đại học')
        ]
        db.session.add_all(ds_yta)
        db.session.commit()
        # # nhan vien---------------------------------------------------------------------------
        ds_nhanvien = [
            NhanVien(id=25, bangCap='Đại học'),
            NhanVien(id=26, bangCap='Thạc sĩ'),
            NhanVien(id=27, bangCap='Đại học'),
        ]
        db.session.add_all(ds_nhanvien)
        db.session.commit()
        # #quan tri--------------------------------------------------------------------------------
        ds_admin = [
            NhanVien(id=28, bangCap='Đại học'),
            NhanVien(id=29, bangCap='Thạc sĩ'),
            NhanVien(id=30, bangCap='Đại học'),
        ]
        db.session.add_all(ds_admin)
        db.session.commit()

        dv1 = DonViThuoc(tenDonVi='chai', moTa='chai ')
        dv2 = DonViThuoc(tenDonVi='lọ', moTa='lọ')
        dv3 = DonViThuoc(tenDonVi='vỉ', moTa='vỉ')
        db.session.add_all([dv1, dv2, dv3])
        db.session.commit()
        ds_danhmuc = [
            DanhMuc(tenDanhMuc='Đau và Sốt'),
            DanhMuc(tenDanhMuc='Chống Viêm'),
            DanhMuc(tenDanhMuc='Kháng Sinh'),
            DanhMuc(tenDanhMuc='Chống Dị Ứng'),
            DanhMuc(tenDanhMuc='Chống Axit Dạ Dày'),
            DanhMuc(tenDanhMuc='Đối Kháng'),
            DanhMuc(tenDanhMuc='Diverse'),
        ]
        db.session.add_all(ds_danhmuc)
        db.session.commit()
        # thuóc
        ds_thuoc = [
            Thuoc(tenThuoc='Paracetamol', moTa='Giảm sốt', gia=91770, trangThai=True, don_vi_thuoc_id=3, danh_muc_id=1),
            Thuoc(tenThuoc='Aspirin', moTa='Giảm đau', gia=137770, trangThai=True, don_vi_thuoc_id=1, danh_muc_id=1),
            Thuoc(tenThuoc='Ibuprofen', moTa='Chống viêm', gia=183770, trangThai=True, don_vi_thuoc_id=3,
                  danh_muc_id=2),
            Thuoc(tenThuoc='Amoxicillin', moTa='Kháng sinh', gia=298770, trangThai=True, don_vi_thuoc_id=2,
                  danh_muc_id=3),
            Thuoc(tenThuoc='Cetirizine', moTa='Chống dị ứng', gia=206770, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=4),
            Thuoc(tenThuoc='Loratadine', moTa='Chống dị ứng', gia=229770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=4),
            Thuoc(tenThuoc='Omeprazole', moTa='Chống axit dạ dày', gia=367770, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=5),
            Thuoc(tenThuoc='Simvastatin', moTa='Giảm cholesterol', gia=275770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=7),
            Thuoc(tenThuoc='Metformin', moTa='Thuốc đối kháng đường huyết', gia=252770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=6),
            Thuoc(tenThuoc='Hydrochlorothiazide', moTa='Thuốc lợi tiểu', gia=344770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=7),
            Thuoc(tenThuoc='Ibuprofen-vs2', moTa='Chống viêm', gia=183770, trangThai=True, don_vi_thuoc_id=3,
                  danh_muc_id=2),
            Thuoc(tenThuoc='Cephalosporin', moTa='Kháng sinh', gia=394770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=3),
            Thuoc(tenThuoc='Efferalgan', moTa='Chống dị ứng', gia=406770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=4),
            Thuoc(tenThuoc='Corticoid', moTa='Chống dị ứng', gia=319770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=4),
            Thuoc(tenThuoc='Lansoprazole', moTa='Chống axit dạ dày', gia=351470, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=5),
            Thuoc(tenThuoc='Lipitor', moTa='Giảm cholesterol', gia=275770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=7),
            Thuoc(tenThuoc='Thiazolidinedione', moTa='Thuốc đối kháng đường huyết', gia=252770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=6),
            Thuoc(tenThuoc='Spironolactone', moTa='Thuốc lợi tiểu', gia=454770, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=7),
            Thuoc(tenThuoc='Atorvastatin', moTa='Giảm cholesterol', gia=321770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=7),
            Thuoc(tenThuoc='Levothyroxine', moTa='Thuốc nội tiết', gia=389770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=7),
            Thuoc(tenThuoc='Prednisone', moTa='Corticosteroid', gia=436770, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=7),
            Thuoc(tenThuoc='Warfarin', moTa='Chống đông máu', gia=481770, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=7),
            Thuoc(tenThuoc='Ciprofloxacin', moTa='Kháng sinh', gia=528770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=3),
            Thuoc(tenThuoc='Diazepam', moTa='Thuốc an thần', gia=573770, trangThai=True, don_vi_thuoc_id=3,
                  danh_muc_id=7),
            Thuoc(tenThuoc='Enalapril', moTa='Chống tăng huyết áp', gia=618770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=7),
            Thuoc(tenThuoc='Gabapentin', moTa='Thuốc an thần', gia=663770, trangThai=True,
                  don_vi_thuoc_id=3, danh_muc_id=7),
            Thuoc(tenThuoc='Hydralazine', moTa='Chống tăng huyết áp', gia=708770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=7),
            Thuoc(tenThuoc='Isoniazid', moTa='Kháng sinh', gia=753770, trangThai=True, don_vi_thuoc_id=3,
                  danh_muc_id=3),
            Thuoc(tenThuoc='Ketoconazole', moTa='Thuốc chống nấm', gia=798770, trangThai=True,
                  don_vi_thuoc_id=1, danh_muc_id=7),
            Thuoc(tenThuoc='Lisinopril', moTa='Chống tăng huyết áp', gia=843770, trangThai=True,
                  don_vi_thuoc_id=2, danh_muc_id=7)

        ]
        db.session.add_all(ds_thuoc)
        db.session.commit()
        #
        ds_dk = [
            DanhSachDangKy(ngayDK=date(2023, 1, 4), ngayHen=date(2023, 1, 9), benh_nhan_id=1),
            DanhSachDangKy(ngayDK=date(2023, 1, 4), ngayHen=date(2023, 1, 9), benh_nhan_id=1),
            DanhSachDangKy(ngayDK=date(2023, 2, 8), ngayHen=date(2023, 2, 13), benh_nhan_id=2),
            DanhSachDangKy(ngayDK=date(2023, 3, 15), ngayHen=date(2023, 3, 20), benh_nhan_id=3),
            DanhSachDangKy(ngayDK=date(2023, 4, 22), ngayHen=date(2023, 4, 27), benh_nhan_id=4),
            DanhSachDangKy(ngayDK=date(2023, 5, 7), ngayHen=date(2023, 5, 12), benh_nhan_id=5),
            DanhSachDangKy(ngayDK=date(2023, 6, 10), ngayHen=date(2023, 6, 15), benh_nhan_id=6),
            DanhSachDangKy(ngayDK=date(2023, 7, 19), ngayHen=date(2023, 7, 24), benh_nhan_id=7),
            DanhSachDangKy(ngayDK=date(2023, 8, 26), ngayHen=date(2023, 8, 31), benh_nhan_id=8),
            DanhSachDangKy(ngayDK=date(2023, 9, 3), ngayHen=date(2023, 9, 8), benh_nhan_id=9),
            DanhSachDangKy(ngayDK=date(2023, 10, 12), ngayHen=date(2023, 10, 17), benh_nhan_id=10),
            DanhSachDangKy(ngayDK=date(2023, 11, 21), ngayHen=date(2023, 11, 26), benh_nhan_id=11),
            DanhSachDangKy(ngayDK=date(2023, 12, 5), ngayHen=date(2023, 12, 10), benh_nhan_id=12),
            DanhSachDangKy(ngayDK=date(2024, 1, 9), ngayHen=date(2024, 1, 14), benh_nhan_id=1),
            DanhSachDangKy(ngayDK=date(2024, 2, 17), ngayHen=date(2024, 2, 22), benh_nhan_id=2),
            DanhSachDangKy(ngayDK=date(2024, 3, 25), ngayHen=date(2024, 3, 30), benh_nhan_id=3),
        ]
        db.session.add_all(ds_dk)
        db.session.commit()
        ds_kham = [
            DanhSachKham(id=1, ngayKham=date(2023, 2, 6)),
            DanhSachKham(id=2, ngayKham=date(2023, 2, 6)),
            DanhSachKham(id=3, ngayKham=date(2023, 3, 15)),
            DanhSachKham(id=4, ngayKham=date(2023, 4, 22)),
            DanhSachKham(id=5, ngayKham=date(2023, 5, 7)),
            DanhSachKham(id=6, ngayKham=date(2023, 6, 10)),
            DanhSachKham(id=7, ngayKham=date(2024, 7, 19)),
            DanhSachKham(id=8, ngayKham=date(2024, 8, 26)),
            DanhSachKham(id=9, ngayKham=date(2024, 9, 3)),
            DanhSachKham(id=10, ngayKham=date(2024, 10, 12)),
            DanhSachKham(id=11, ngayKham=date(2024, 11, 21)),
            DanhSachKham(id=12, ngayKham=date(2024, 1, 9)),
            DanhSachKham(id=13, ngayKham=date(2024, 2, 17)),
            DanhSachKham(id=14, ngayKham=date(2024, 3, 25)),
            DanhSachKham(id=15, ngayKham=date(2024, 4, 1)),
            DanhSachKham(id=16, ngayKham=date(2024, 5, 15))
        ]
        db.session.add_all(ds_kham)
        db.session.commit()
        #
        ds_ct = [
            ChiTietDanhSach(danhSachKham_id=1, is_active=1, benhNhan_id=1, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=2, is_active=1, benhNhan_id=2, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=3, is_active=1, benhNhan_id=3, bacSi_id=15),
            ChiTietDanhSach(danhSachKham_id=4, is_active=1, benhNhan_id=4, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=5, is_active=1, benhNhan_id=5, bacSi_id=17),
            ChiTietDanhSach(danhSachKham_id=6, is_active=1, benhNhan_id=6, bacSi_id=18),
            ChiTietDanhSach(danhSachKham_id=7, is_active=1, benhNhan_id=7, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=8, is_active=1, benhNhan_id=8, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=9, is_active=1, benhNhan_id=9, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=10, is_active=1, benhNhan_id=10, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=11, is_active=1, benhNhan_id=11, bacSi_id=16),
            ChiTietDanhSach(danhSachKham_id=12, is_active=1, benhNhan_id=12, bacSi_id=17),
            ChiTietDanhSach(danhSachKham_id=13, is_active=1, benhNhan_id=1, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=14, is_active=1, benhNhan_id=2, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=15, is_active=1, benhNhan_id=3, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=16, is_active=1, benhNhan_id=4, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=1, is_active=1, benhNhan_id=5, bacSi_id=15),
            ChiTietDanhSach(danhSachKham_id=2, is_active=1, benhNhan_id=6, bacSi_id=16),
            ChiTietDanhSach(danhSachKham_id=3, is_active=1, benhNhan_id=7, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=4, is_active=1, benhNhan_id=8, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=5, is_active=1, benhNhan_id=9, bacSi_id=19),
            ChiTietDanhSach(danhSachKham_id=6, is_active=1, benhNhan_id=10, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=7, is_active=1, benhNhan_id=11, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=8, is_active=1, benhNhan_id=12, bacSi_id=15),
            ChiTietDanhSach(danhSachKham_id=9, is_active=1, benhNhan_id=1, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=10, is_active=1, benhNhan_id=2, bacSi_id=17),
            ChiTietDanhSach(danhSachKham_id=11, is_active=1, benhNhan_id=3, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=12, is_active=1, benhNhan_id=4, bacSi_id=19),
            ChiTietDanhSach(danhSachKham_id=13, is_active=1, benhNhan_id=5, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=14, is_active=1, benhNhan_id=6, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=15, is_active=1, benhNhan_id=7, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=16, is_active=1, benhNhan_id=8, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=1, is_active=1, benhNhan_id=9, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=2, is_active=1, benhNhan_id=10, bacSi_id=18),
            ChiTietDanhSach(danhSachKham_id=3, is_active=1, benhNhan_id=11, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=4, is_active=1, benhNhan_id=12, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=5, is_active=1, benhNhan_id=1, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=6, is_active=1, benhNhan_id=2, bacSi_id=15),
            ChiTietDanhSach(danhSachKham_id=7, is_active=1, benhNhan_id=3, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=8, is_active=1, benhNhan_id=4, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=9, is_active=1, benhNhan_id=5, bacSi_id=18),
            ChiTietDanhSach(danhSachKham_id=10, is_active=1, benhNhan_id=6, bacSi_id=19),
            ChiTietDanhSach(danhSachKham_id=11, is_active=1, benhNhan_id=7, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=12, is_active=1, benhNhan_id=8, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=13, is_active=1, benhNhan_id=9, bacSi_id=15),
            ChiTietDanhSach(danhSachKham_id=14, is_active=1, benhNhan_id=10, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=15, is_active=1, benhNhan_id=11, bacSi_id=17),
            ChiTietDanhSach(danhSachKham_id=16, is_active=1, benhNhan_id=12, bacSi_id=18),
            ChiTietDanhSach(danhSachKham_id=1, is_active=1, benhNhan_id=1, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=2, is_active=1, benhNhan_id=2, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=3, is_active=1, benhNhan_id=3, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=4, is_active=1, benhNhan_id=4, bacSi_id=13),
            ChiTietDanhSach(danhSachKham_id=5, is_active=1, benhNhan_id=5, bacSi_id=16),
            ChiTietDanhSach(danhSachKham_id=6, is_active=1, benhNhan_id=6, bacSi_id=17),
            ChiTietDanhSach(danhSachKham_id=7, is_active=1, benhNhan_id=7, bacSi_id=14),
            ChiTietDanhSach(danhSachKham_id=8, is_active=1, benhNhan_id=8, bacSi_id=19),
        ]
        db.session.add_all(ds_ct)
        db.session.commit()
        ds_pk=[
            PhieuKham(id=1, chuanDoan='Cảm, sốt', trieuChung='Đau đầu', ngayKham=date(2023, 8, 3), benh_nhan_id=1),
            PhieuKham(id=2, chuanDoan='Viêm họng', trieuChung='Đau họng', ngayKham=date(2023, 1, 5), benh_nhan_id=2),
            PhieuKham(id=3, chuanDoan='Sổ mũi', trieuChung='Chảy nước mũi', ngayKham=date(2023, 11, 7), benh_nhan_id=3),
            PhieuKham(id=4, chuanDoan='Tiêu chảy', trieuChung='Đau bụng', ngayKham=date(2023, 12, 9), benh_nhan_id=4),
            PhieuKham(id=5, chuanDoan='Gãy chân', trieuChung='Đau chân', ngayKham=date(2023, 2, 11), benh_nhan_id=5),
            PhieuKham(id=6, chuanDoan='Mệt mỏi', trieuChung='Khó thở', ngayKham=date(2023, 1, 13), benh_nhan_id=6),
            PhieuKham(id=7, chuanDoan='Sỏi thận', trieuChung='Đau lưng', ngayKham=date(2023, 7, 15), benh_nhan_id=7),
            PhieuKham(id=8, chuanDoan='Đau răng', trieuChung='Đau răng', ngayKham=date(2023, 4, 17), benh_nhan_id=8),
            PhieuKham(id=9, chuanDoan='Viêm gan', trieuChung='Mệt mỏi', ngayKham=date(2023, 8, 19), benh_nhan_id=9),
            PhieuKham(id=10, chuanDoan='Thủy thũng', trieuChung='Sưng nước mắt', ngayKham=date(2024, 9, 21),benh_nhan_id=10),
            PhieuKham(id=11, chuanDoan='Viêm gan', trieuChung='Mệt mỏi', ngayKham=date(2023, 12, 23), benh_nhan_id=11),
            PhieuKham(id=12, chuanDoan='Đau răng', trieuChung='Đau răng', ngayKham=date(2024, 3, 25), benh_nhan_id=12),
            PhieuKham(id=13, chuanDoan='Sỏi thận', trieuChung='Đau lưng', ngayKham=date(2024, 4, 27), benh_nhan_id=1),
            PhieuKham(id=14, chuanDoan='Mệt mỏi', trieuChung='Khó thở', ngayKham=date(2024, 2, 29), benh_nhan_id=2),
            PhieuKham(id=15, chuanDoan='Gãy chân', trieuChung='Đau chân', ngayKham=date(2024, 3, 1), benh_nhan_id=3),
            PhieuKham(id=16, chuanDoan='Tiêu chảy', trieuChung='Đau bụng', ngayKham=date(2024, 5, 3), benh_nhan_id=4),
            PhieuKham(id=17, chuanDoan='Sổ mũi', trieuChung='Chảy nước mũi', ngayKham=date(2024, 6, 5), benh_nhan_id=5),
            PhieuKham(id=18, chuanDoan='Viêm họng', trieuChung='Đau họng', ngayKham=date(2024, 9, 7), benh_nhan_id=6),
            PhieuKham(id=19, chuanDoan='Cảm, sốt', trieuChung='Đau đầu', ngayKham=date(2024, 10, 9), benh_nhan_id=7),
            PhieuKham(id=20, chuanDoan='Thủy thũng', trieuChung='Sưng nước mắt', ngayKham=date(2024, 11, 11),benh_nhan_id=8)
        ]
        db.session.add_all(ds_pk)
        db.session.commit()

        ds_phieuthuoc=[
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=1, thuoc_id=2),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=1, thuoc_id=4),
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=2, thuoc_id=12),
            PhieuThuoc(soLuong=3, cachDung='2/ngày', phieu_kham_id=3, thuoc_id=1),
            PhieuThuoc(soLuong=1, cachDung='1/ngày', phieu_kham_id=4, thuoc_id=16),
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=2, thuoc_id=25),
            PhieuThuoc(soLuong=3, cachDung='3/ngày', phieu_kham_id=3, thuoc_id=14),
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=4, thuoc_id=18),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=5, thuoc_id=5),
            PhieuThuoc(soLuong=1, cachDung='1/ngày', phieu_kham_id=6, thuoc_id=4),
            PhieuThuoc(soLuong=3, cachDung='1/ngày', phieu_kham_id=7, thuoc_id=9),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=7, thuoc_id=10),
            PhieuThuoc(soLuong=3, cachDung='3/ngày', phieu_kham_id=8, thuoc_id=14),
            PhieuThuoc(soLuong=1, cachDung='1/ngày', phieu_kham_id=8, thuoc_id=27),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=9, thuoc_id=3),
            PhieuThuoc(soLuong=2, cachDung='3/ngày', phieu_kham_id=9, thuoc_id=13),
            PhieuThuoc(soLuong=3, cachDung='2/ngày', phieu_kham_id=10, thuoc_id=20),
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=11, thuoc_id=7),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=12, thuoc_id=6),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=13, thuoc_id=2),
            PhieuThuoc(soLuong=1, cachDung='1/ngày', phieu_kham_id=13, thuoc_id=19),
            PhieuThuoc(soLuong=3, cachDung='2/ngày', phieu_kham_id=14, thuoc_id=22),
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=15, thuoc_id=21),
            PhieuThuoc(soLuong=1, cachDung='2/ngày', phieu_kham_id=16, thuoc_id=17),
            PhieuThuoc(soLuong=2, cachDung='1/ngày', phieu_kham_id=17, thuoc_id=27),
            PhieuThuoc(soLuong=3, cachDung='2/ngày', phieu_kham_id=18, thuoc_id=30),
            PhieuThuoc(soLuong=1, cachDung='1/ngày', phieu_kham_id=19, thuoc_id=14),
            PhieuThuoc(soLuong=2, cachDung='3/ngày', phieu_kham_id=19, thuoc_id=25),
            PhieuThuoc(soLuong=4, cachDung='1/ngày', phieu_kham_id=20, thuoc_id=26),
            PhieuThuoc(soLuong=2, cachDung='2/ngày', phieu_kham_id=20, thuoc_id=20)
        ]
        db.session.add_all(ds_phieuthuoc)
        db.session.commit()


