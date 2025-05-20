<?php

namespace App\Http\Controllers;

use App\Models\FactVehicleCount;
use App\Http\Resources\FactVehicleCountResource;
use Illuminate\Support\Facades\DB;

class FactVehicleCountController extends Controller
{
    public function index()
    {
        $factVehicleCounts = FactVehicleCount::with(['date', 'time', 'location'])->get();

        return FactVehicleCountResource::collection($factVehicleCounts);
    }
    public function getTotalVehicleCount()
    {
        $totalVehicleCount = FactVehicleCount::sum('car') + FactVehicleCount::sum('motorcycle') + FactVehicleCount::sum('bike') + FactVehicleCount::sum('truck') + FactVehicleCount::sum('bus');

        return response()->json(['total_vehicle_count' => $totalVehicleCount]);
    }
    public function getTotalCarCount()
    {
        $totalCarCount = FactVehicleCount::sum('car');

        return response()->json(['total_car_count' => $totalCarCount]);
    }
    public function getTotalMotorcycleCount()
    {
        $totalMotorcycleCount = FactVehicleCount::sum('motorcycle');

        return response()->json(['total_motorcycle_count' => $totalMotorcycleCount]);
    }
    public function getTotalBikeCount()
    {
        $totalBikeCount = FactVehicleCount::sum('bike');

        return response()->json(['total_bike_count' => $totalBikeCount]);
    }
    public function getTotalTruckCount()
    {
        $totalTruckCount = FactVehicleCount::sum('truck');

        return response()->json(['total_truck_count' => $totalTruckCount]);
    }
    public function getTotalBusCount()
    {
        $totalBusCount = FactVehicleCount::sum('bus');

        return response()->json(['total_bus_count' => $totalBusCount]);
    }
    public function getMustMovimentedStreets()
    {
        $mustMovimentedStreets = FactVehicleCount::join('warehouse_vehicle_count_db.dim_location', 'fact_vehicle_counts.location_id', '=', 'dim_location.location_id')
            ->select('dim_location.location as location_name', DB::raw('SUM(car + motorcycle + bike + truck + bus) as total'))
            ->groupBy('dim_location.location')
            ->orderBy('total', 'desc')
            ->take(5)
            ->get();
    
        return response()->json([
            'most_movimented_stress' => $mustMovimentedStreets
        ]);
    }
    public function getLessMovimentedStreets()
    {
        $lessMovimentedStreets = FactVehicleCount::join('warehouse_vehicle_count_db.dim_location', 'fact_vehicle_counts.location_id', '=', 'dim_location.location_id')
            ->select('dim_location.location as location_name', DB::raw('SUM(car + motorcycle + bike + truck + bus) as total'))
            ->groupBy('dim_location.location')
            ->orderBy('total', 'asc')
            ->take(5)
            ->get();
    
        return response()->json([
            'less_movimented_stress' => $lessMovimentedStreets
        ]);
    }
}
