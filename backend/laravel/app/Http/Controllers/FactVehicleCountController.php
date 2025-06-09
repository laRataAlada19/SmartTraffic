<?php

namespace App\Http\Controllers;

use App\Models\FactVehicleCount;
use App\Http\Resources\FactVehicleCountResource;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;
use Carbon\Carbon;

class FactVehicleCountController extends Controller
{
    public function index()
    {
        $factVehicleCounts = FactVehicleCount::with(['date', 'time', 'location'])->get();

        return FactVehicleCountResource::collection($factVehicleCounts);
    }

    public function totalVehicles(Request $request)
    {
        return response()->json([
            'total_vehicle_count' => $this->aggregateData($request, '*')
        ]);
    }

    public function totalCars(Request $request)
    {
        return response()->json([
            'total_car_count' => $this->aggregateData($request, 'car')
        ]);
    }

    public function totalBikes(Request $request)
    {
        return response()->json([
            'total_bike_count' => $this->aggregateData($request, 'bike')
        ]);
    }

    public function totalTrucks(Request $request)
    {
        return response()->json([
            'total_truck_count' => $this->aggregateData($request, 'truck')
        ]);
    }

    public function totalBuses(Request $request)
    {
        return response()->json([
            'total_bus_count' => $this->aggregateData($request, 'bus')
        ]);
    }

    public function totalMotorcycles(Request $request)
    {
        return response()->json([
            'total_motorcycle_count' => $this->aggregateData($request, 'motorcycle')
        ]);
    }

    public function mostMovimented(Request $request)
    {
        $data = $this->aggregateByLocation($request, 'desc');
        return response()->json([
            'most_movimented_stress' => $data
        ]);
    }

    public function lessMovimented(Request $request)
    {
        $data = $this->aggregateByLocation($request, 'asc');
        return response()->json([
            'less_movimented_stress' => $data
        ]);
    }

    private function aggregateData(Request $request, $vehicleType)
    {
        $date = Carbon::parse($request->input('date'));
        $theme = $request->input('theme', 1);
    
        switch ($theme) {
            case 2:
                $start = $date->copy()->startOfWeek();
                $end = $date->copy()->endOfWeek();
                break;
            case 3:
                $start = $date->copy()->startOfMonth();
                $end = $date->copy()->endOfMonth();
                break;
            case 4:
                $start = $date->copy()->startOfYear();
                $end = $date->copy()->endOfYear();
                break;
            default:
                $start = $date->copy()->startOfDay();
                $end = $date->copy()->endOfDay();
                break;
        }
    
        $query = DB::table('warehouse_vehicle_count_db.fact_vehicle_counts as f')
            ->join('warehouse_vehicle_count_db.dim_date as d', 'f.date_id', '=', 'd.date_id')
            ->whereBetween('d.full_date', [$start->toDateString(), $end->toDateString()]);
    
        if ($vehicleType === '*') {
            $total = $query->select(DB::raw('SUM(car + motorcycle + bike + truck + bus) as total'))->value('total');
            return $total ?? 0;
        } else {
            $total = $query->sum($vehicleType);
            return $total ?? 0;
        }
    }
    

    private function aggregateByLocation(Request $request, $order)
    {
        $date = Carbon::parse($request->input('date'));
        $theme = $request->input('theme', 1);

        switch ($theme) {
            case 2:
                $start = $date->copy()->startOfWeek();
                $end = $date->copy()->endOfWeek();
                break;
            case 3:
                $start = $date->copy()->startOfMonth();
                $end = $date->copy()->endOfMonth();
                break;
            case 4:
                $start = $date->copy()->startOfYear();
                $end = $date->copy()->endOfYear();
                break;
            default:
                $start = $date->copy()->startOfDay();
                $end = $date->copy()->endOfDay();
                break;
        }

        $result = DB::table('warehouse_vehicle_count_db.fact_vehicle_counts as f')
            ->join('warehouse_vehicle_count_db.dim_date as d', 'f.date_id', '=', 'd.date_id')
            ->join('warehouse_vehicle_count_db.dim_location as l', 'f.location_id', '=', 'l.location_id')
            ->whereBetween('d.full_date', [$start->toDateString(), $end->toDateString()])
            ->select('l.location as location_name', DB::raw('SUM(car + motorcycle + bike + truck + bus) as total'))
            ->groupBy('l.location')
            ->orderBy('total', $order)
            ->limit(1)
            ->get();

        return $result;
    }
}
