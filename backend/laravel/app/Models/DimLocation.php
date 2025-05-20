<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DimLocation extends Model
{
    protected $connection = 'dw_pgsql';
    protected $table = 'warehouse_vehicle_count_db.dim_location';
}