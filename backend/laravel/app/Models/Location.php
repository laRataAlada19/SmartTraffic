<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Location extends Model
{
    use HasFactory;

    protected $fillable = [
        'location', 
        'direction',
        'latitude',
        'longitude'
    ];

    protected $table = 'vehicle_detection.locations';


    public $timestamps = false;
    protected $primaryKey = 'location_id';
    public $incrementing = true;
    protected $keyType = 'integer';
}